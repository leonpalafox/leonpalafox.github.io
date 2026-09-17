#!/usr/bin/env python3
"""Self-contained tests for the poll-of-polls pipeline.

Run with ``python3 -m unittest discover -s tests -v`` (or ``python3 tests/test_pollofpolls.py``).
No third-party packages, no network, no fixtures on disk: every HTML sample is
inlined so a broken parser fails here rather than in a published chart.
"""

from __future__ import annotations

import math
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from pollofpolls import sources, stats, teams, validate  # noqa: E402


class TestTeamResolution(unittest.TestCase):
    def test_full_names(self):
        self.assertEqual(teams.normalize("Seattle Seahawks"), "Seattle Seahawks")
        self.assertEqual(teams.normalize("seattle seahawks"), "Seattle Seahawks")

    def test_nicknames_and_abbreviations(self):
        self.assertEqual(teams.normalize("49ers"), "San Francisco 49ers")
        self.assertEqual(teams.normalize("SF"), "San Francisco 49ers")
        self.assertEqual(teams.normalize("L.A. Rams"), "Los Angeles Rams")
        self.assertEqual(teams.normalize("Jags"), "Jacksonville Jaguars")

    def test_noise_is_rejected(self):
        self.assertIsNone(teams.normalize("Caret Up"))
        self.assertIsNone(teams.normalize("Rank increased by"))
        self.assertIsNone(teams.normalize(""))

    def test_plural_city_collisions_stay_distinct(self):
        self.assertEqual(teams.normalize("New York Jets"), "New York Jets")
        self.assertEqual(teams.normalize("New York Giants"), "New York Giants")


class TestDistributionMath(unittest.TestCase):
    def test_uniform_rank_moments(self):
        # 1..32: mean 16.5, sd sqrt((32^2-1)/12)
        self.assertAlmostEqual(stats.uniform_rank_mean(32), 16.5)
        self.assertAlmostEqual(stats.uniform_rank_sd(32), math.sqrt((32**2 - 1) / 12))

    def test_normal_quantile(self):
        self.assertAlmostEqual(stats._normal_quantile(0.975), 1.959964, places=4)
        self.assertAlmostEqual(stats._normal_quantile(0.5), 0.0, places=6)
        self.assertAlmostEqual(stats._normal_quantile(0.025), -1.959964, places=4)

    def test_t_quantile_matches_published_values(self):
        self.assertAlmostEqual(stats._t_quantile(0.975, 8), 2.306, places=2)
        self.assertAlmostEqual(stats._t_quantile(0.975, 30), 2.042, places=2)
        self.assertAlmostEqual(stats._t_quantile(0.95, 10), 1.812, places=2)

    def test_spearman(self):
        self.assertAlmostEqual(stats.spearman([1, 2, 3, 4], [1, 2, 3, 4]), 1.0)
        self.assertAlmostEqual(stats.spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)
        # Ties are averaged rather than broken arbitrarily.
        self.assertAlmostEqual(stats.spearman([1, 1, 2], [1, 1, 2]), 1.0)

    def test_percentile_interpolates(self):
        self.assertAlmostEqual(stats.percentile([1, 2, 3, 4], 0.5), 2.5)
        self.assertAlmostEqual(stats.percentile([1, 2, 3, 4], 0.0), 1.0)
        self.assertAlmostEqual(stats.percentile([1, 2, 3, 4], 1.0), 4.0)


def _ballot(order: list[str]) -> dict[str, int]:
    return {team: rank for rank, team in enumerate(order, start=1)}


class TestConsensus(unittest.TestCase):
    def setUp(self):
        self.order = sorted(teams.TEAMS)
        self.n = len(self.order)

    def _rotated(self, shift: int) -> dict[str, int]:
        rotated = self.order[shift:] + self.order[:shift]
        return _ballot(rotated)

    def test_identical_ballots_are_perfectly_consistent(self):
        ballots = {f"src{i}": _ballot(self.order) for i in range(5)}
        panel = stats.build_panel(ballots, teams=self.order)
        rows, diag = stats.consensus(panel, bootstrap=200)
        self.assertEqual([row.rank for row in rows], list(range(1, self.n + 1)))
        self.assertEqual(rows[0].team, self.order[0])
        self.assertAlmostEqual(diag.mean_pairwise_spearman, 1.0)
        # Every team, including the last one, is on the diagonal.
        for row in rows:
            self.assertEqual(row.rank_min, row.rank)
            self.assertEqual(row.rank_max, row.rank)
            self.assertEqual(row.spread, 0)

    def test_scores_are_monotone_in_rank_and_shrunk(self):
        ballots = {f"src{i}": self._rotated(i) for i in range(5)}
        panel = stats.build_panel(ballots, teams=self.order)
        rows, diag = stats.consensus(panel, bootstrap=500)
        scores = [row.score for row in rows]
        self.assertEqual(scores, sorted(scores, reverse=True))
        # Shrinkage compresses the top, so the best score sits below the raw z
        # score a team would get on a perfectly uniform ballot.
        self.assertLess(rows[0].score, 1.4)
        # Ordering by the shrunk score matches ordering by the pooled z.
        by_raw = sorted(rows, key=lambda row: -row.score_raw)
        self.assertEqual([row.team for row in by_raw], [row.team for row in rows])

    def test_uncertainty_is_non_negative_and_ordered(self):
        ballots = {f"src{i}": self._rotated(i * 3) for i in range(6)}
        panel = stats.build_panel(ballots, teams=self.order)
        rows, _ = stats.consensus(panel, bootstrap=300)
        for row in rows:
            self.assertGreaterEqual(row.se, 0.0)
            self.assertLessEqual(row.ci_low, row.score)
            self.assertLessEqual(row.score, row.ci_high)
            self.assertLessEqual(row.rank_ci_low, row.rank)
            self.assertLessEqual(row.rank, row.rank_ci_high)
            self.assertTrue(0.0 <= row.p_top1 <= 1.0)
        self.assertAlmostEqual(sum(row.p_top1 for row in rows), 1.0, places=6)

    def test_contested_team_gets_more_uncertainty(self):
        # Everyone agrees on team 0; two sources fight over team 1.
        base = _ballot(self.order)
        noisy = dict(base)
        noisy[self.order[1]], noisy[self.order[2]] = 3, 2
        ballots = {"a": base, "b": base, "c": base, "d": noisy}
        panel = stats.build_panel(ballots, teams=self.order)
        rows, _ = stats.consensus(panel, bootstrap=400)
        by_team = {row.team: row for row in rows}
        self.assertLess(
            by_team[self.order[0]].se,
            by_team[self.order[1]].se,
        )

    def test_requires_two_complete_ballots(self):
        panel = stats.build_panel({"only": _ballot(self.order)}, teams=self.order)
        with self.assertRaises(ValueError):
            stats.consensus(panel)

    def test_incomplete_ballot_is_dropped_not_imputed(self):
        full = _ballot(self.order)
        partial = {team: rank for team, rank in list(full.items())[:20]}
        panel = stats.build_panel({"full": full, "partial": partial}, teams=self.order)
        self.assertEqual(len(panel.matrix(require_complete=True)), 1)
        self.assertIn("partial", panel.matrix(require_complete=False))


class TestValidation(unittest.TestCase):
    def test_complete_ballot_passes(self):
        ballot = _ballot(sorted(teams.TEAMS))
        self.assertEqual(validate.validate_ballot("ok", ballot), [])

    def test_missing_team_is_an_error(self):
        ballot = _ballot(sorted(teams.TEAMS))
        del ballot["Seattle Seahawks"]
        issues = validate.validate_ballot("short", ballot)
        self.assertTrue(any("missing" in issue.message for issue in issues))

    def test_duplicate_rank_is_an_error(self):
        ballot = _ballot(sorted(teams.TEAMS))
        # Give one club a rank another club already holds, leaving rank 1 free.
        ballot["Arizona Cardinals"] = ballot["Atlanta Falcons"]
        messages = " ".join(issue.message for issue in validate.validate_ballot("dupe", ballot))
        self.assertIn("duplicate", messages)

    def test_too_few_sources_fails_the_panel(self):
        order = sorted(teams.TEAMS)
        ballots = {f"s{i}": _ballot(order) for i in range(4)}
        report = validate.validate_panel(ballots)
        self.assertFalse(report.ok)

    def test_identical_syndicated_copies_are_rejected(self):
        order = sorted(teams.TEAMS)
        ballots = {f"s{i}": _ballot(order) for i in range(5)}
        report = validate.validate_panel(ballots)
        self.assertFalse(report.ok)
        self.assertTrue(any("identical" in issue.message for issue in report.errors))


class TestExtractors(unittest.TestCase):
    """Each extractor is exercised on a minimal, hand-built sample of the
    markup it targets, so a site redesign surfaces here immediately."""

    def _assert_full(self, ballot: dict[str, int]):
        self.assertEqual(len(ballot), 32)
        self.assertEqual(sorted(ballot.values()), list(range(1, 33)))

    def test_nflcom_rank_marker(self):
        rows = []
        for rank, team in enumerate(sorted(teams.TEAMS), start=1):
            rows.append(
                f'<div aria-label="Rank {rank}"><div>Rank</div><div>{rank}</div>'
                f"<span>Caret Up</span><span>Rank increased by</span>"
                f"<a>{team}</a><span>1-0</span></div>"
            )
        ballot = sources.extract("nflcom_rank_marker", "<html>" + "".join(rows) + "</html>")
        self._assert_full(ballot)
        self.assertEqual(ballot["Arizona Cardinals"], 1)

    def test_cbs_table(self):
        rows = []
        for rank, team in enumerate(sorted(teams.TEAMS), start=1):
            rows.append(
                f'<tr class="team-rankings-stats"><td><span class="rank"> {rank} </span></td>'
                f'<td class="cell-left team"><span class="team-name"> {team} </span>'
                f"</td></tr>"
            )
        ballot = sources.extract("cbs_table", "<table>" + "".join(rows) + "</table>")
        self._assert_full(ballot)

    def test_sharp_embedded_table(self):
        ordered = sorted(teams.TEAMS)
        payload = '[["Power Rank","Team","Change"]' + "".join(
            f',["{rank}","{team}","+1"]' for rank, team in enumerate(ordered, start=1)
        ) + "]"
        ballot = sources.extract("sharp_embedded_table", f"<script>{payload}</script>")
        self._assert_full(ballot)

    def test_fox_hash_allows_digit_leading_names(self):
        # FOX prints the rank inside the anchor text, so the assertion is that
        # the parser reads the printed rank (and never position in the page).
        ranked = sorted(teams.TEAMS)
        rows = [
            f'<a class="entity-title text">#{rank} {team}</a>'
            for rank, team in enumerate(ranked, start=1)
        ]
        ballot = sources.extract("fox_hash", "".join(rows))
        self._assert_full(ballot)
        self.assertEqual(
            ballot["San Francisco 49ers"], ranked.index("San Francisco 49ers") + 1
        )
        self.assertEqual(ballot["Arizona Cardinals"], 1)

    def test_fox_hash_reads_rank_not_position(self):
        # A 32 -> 1 page must not be silently reversed: the last card is #1.
        ranked = sorted(teams.TEAMS)
        rows = [
            f'<a class="entity-title text">#{rank} {team}</a>'
            for rank, team in enumerate(reversed(ranked), start=1)
        ]
        ballot = sources.extract("fox_hash", "".join(rows))
        self.assertEqual(ballot["Arizona Cardinals"], len(ranked))
        self.assertEqual(ballot["San Francisco 49ers"], len(ranked) - ranked.index("San Francisco 49ers"))

    def test_numbered_table_skips_prose(self):
        # Prose mentioning a rank must not be picked up as a table row.
        prose = "<p>In Week 2, 3 teams stood out and 24 points were scored.</p>"
        rows = "".join(
            f"<p>{rank}. <a>{team}</a> (previous rank: {rank}):</p>"
            for rank, team in enumerate(sorted(teams.TEAMS), start=1)
        )
        ballot = sources.extract("si_numbered", prose + rows)
        self._assert_full(ballot)

    def test_reynolds_ordered_list_without_start_attribute(self):
        rows = []
        for rank, team in enumerate(sorted(teams.TEAMS), start=1):
            if rank == 1:
                rows.append(f"<ol><li><strong>{team} --</strong></li></ol>")
            else:
                rows.append(f'<ol start="{rank}"><li><strong>{team} +2</strong></li></ol>')
        rows.append("<ol><li>Unrelated sidebar</li></ol>")
        ballot = sources.extract("nflcom_reynolds", "".join(rows))
        self._assert_full(ballot)
        self.assertEqual(ballot[sorted(teams.TEAMS)[0]], 1)
        self.assertEqual(ballot[sorted(teams.TEAMS)[5]], 6)

    def test_unknown_extractor_raises(self):
        with self.assertRaises(KeyError):
            sources.extract("does_not_exist", "<html></html>")




class TestHeadToHead(unittest.TestCase):
    def setUp(self):
        from pollofpolls import headtohead

        self.h2h = headtohead
        self.model = headtohead.Model(k=4.59, home_field=2.56, sigma=13.16)

    def test_normal_cdf_endpoints(self):
        self.assertAlmostEqual(self.h2h.normal_cdf(0.0), 0.5, places=9)
        self.assertAlmostEqual(self.h2h.normal_cdf(1.959964), 0.975, places=5)
        self.assertAlmostEqual(self.h2h.normal_cdf(-1.959964), 0.025, places=5)

    def test_equal_teams_give_home_edge(self):
        probability = self.h2h.home_win_probability(1.0, 1.0, self.model)
        self.assertGreater(probability, 0.5)
        # The edge is exactly the home-field term over sigma.
        self.assertAlmostEqual(
            probability, self.h2h.normal_cdf(self.model.home_field / self.model.sigma), places=9
        )

    def test_neutral_site_removes_home_edge(self):
        self.assertAlmostEqual(
            self.h2h.home_win_probability(1.0, 1.0, self.model, neutral=True), 0.5, places=9
        )

    def test_better_team_is_favoured(self):
        strong = self.h2h.predict("Seattle Seahawks", "Cleveland Browns",
                                 {"Seattle Seahawks": 1.5, "Cleveland Browns": -1.5}, self.model)
        self.assertGreater(strong["homeWinProbability"], 0.5)
        self.assertEqual(strong["favourite"], "Seattle Seahawks")
        self.assertEqual(strong["pick"], "SEA by 16.3")

    def test_probabilities_sum_to_one(self):
        record = self.h2h.predict("Chicago Bears", "Green Bay Packers",
                                  {"Chicago Bears": 0.9, "Green Bay Packers": -0.1}, self.model)
        self.assertAlmostEqual(
            record["homeWinProbability"] + record["awayWinProbability"], 1.0, places=12
        )

    def test_margin_sign_matches_favourite(self):
        away_better = self.h2h.predict("Cleveland Browns", "Seattle Seahawks",
                                       {"Seattle Seahawks": 1.5, "Cleveland Browns": -1.5}, self.model)
        self.assertLess(away_better["expectedMargin"], 0)
        self.assertEqual(away_better["favourite"], "Seattle Seahawks")
        self.assertLess(away_better["homeWinProbability"], 0.5)

    def test_unknown_team_raises(self):
        with self.assertRaises(KeyError):
            self.h2h.predict("Seattle Seahawks", "Nowhere FC",
                             {"Seattle Seahawks": 1.0}, self.model)

    def test_default_model_matches_calibration(self):
        from pollofpolls import headtohead

        self.assertAlmostEqual(headtohead.DEFAULT_MODEL.k, 4.59, places=2)
        self.assertAlmostEqual(headtohead.DEFAULT_MODEL.sigma, 13.16, places=2)

    def test_scoring_rules(self):
        self.assertAlmostEqual(self.h2h.brier_score(0.9, True), 0.01, places=9)
        self.assertAlmostEqual(self.h2h.brier_score(0.1, False), 0.01, places=9)
        self.assertLess(self.h2h.log_loss(0.9, True), self.h2h.log_loss(0.6, True))

    def test_calibration_table_buckets(self):
        records = [(0.55, True)] * 10 + [(0.95, True)] * 10 + [(0.95, False)] * 10
        table = self.h2h.calibration_table(records, buckets=5)
        self.assertEqual(sum(row["n"] for row in table), 30)
        top = table[-1]
        self.assertGreater(top["low"], 0.85)
        self.assertAlmostEqual(top["observed"], 0.5, places=6)


class TestSchedule(unittest.TestCase):
    NFLVERSE_SAMPLE = (
        "game_id,season,game_type,week,gameday,gametime,away_team,home_team,"
        "away_score,home_score,location,spread_line,stadium\n"
        "1,2026,REG,2,2026-09-17,20:15,DET,BUF,,,Home,4.5,Highmark Stadium\n"
        "2,2026,REG,2,2026-09-20,13:00,CAR,ATL,,,Home,-2.5,Mercedes-Benz Stadium\n"
        "3,2026,REG,2,2026-09-20,16:25,MIA,SF,,,Home,13.5,Levi's Stadium\n"
        "4,2026,REG,2,2026-09-21,20:15,NYG,LA,,,Neutral,7.0,SoFi Stadium\n"
        "5,2026,REG,3,2026-09-24,20:15,SEA,ARI,,,Home,-3.5,State Farm Stadium\n"
        "6,2025,REG,2,2025-09-14,13:00,SEA,NE,10,13,Home,-1.5,Gillette Stadium\n"
    )

    def test_parses_only_the_requested_week(self):
        from pollofpolls import games

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2026, week=2)
        self.assertEqual(len(slate), 4)
        self.assertEqual({(g.away, g.home) for g in slate},
                         {("Detroit Lions", "Buffalo Bills"),
                          ("Carolina Panthers", "Atlanta Falcons"),
                          ("Miami Dolphins", "San Francisco 49ers"),
                          ("New York Giants", "Los Angeles Rams")})

    def test_reads_kickoff_spread_and_venue(self):
        from pollofpolls import games

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2026, week=2)
        det = next(g for g in slate if g.away == "Detroit Lions")
        self.assertEqual(det.gameday, "2026-09-17")
        self.assertEqual(det.kickoff, "20:15")
        self.assertEqual(det.spread, 4.5)
        self.assertEqual(det.venue, "Highmark Stadium")
        self.assertFalse(det.played)

    def test_neutral_site_detected(self):
        from pollofpolls import games

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2026, week=2)
        giants = next(g for g in slate if g.away == "New York Giants")
        self.assertTrue(giants.neutral)
        self.assertTrue(all(not g.neutral for g in slate if g.away != "New York Giants"))

    def test_played_game_exposes_margin(self):
        from pollofpolls import games

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2025, week=2)
        self.assertEqual(len(slate), 1)
        self.assertTrue(slate[0].played)
        self.assertEqual(slate[0].margin, 3)

    def test_sorted_by_kickoff(self):
        from pollofpolls import games

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2026, week=2)
        keys = [(g.gameday, g.kickoff) for g in slate]
        self.assertEqual(keys, sorted(keys))

    def test_nflcom_fallback_handles_digit_leading_names(self):
        from pollofpolls import games

        html = (
            '<a data-analytics="{&quot;linkName&quot;:&quot;Lions at Bills, '
            'Thursday, September 17th, 8:15 PM, GamePass&quot;}"></a>'
            '<a data-analytics="{&quot;linkName&quot;:&quot;Dolphins at 49ers, '
            'Sunday, September 20th, 4:25 PM, GamePass&quot;}"></a>'
        )
        slate = games.parse_nflcom_schedule(html, season=2026, week=2)
        self.assertEqual(len(slate), 2)
        forty_niners = next(g for g in slate if g.home == "San Francisco 49ers")
        self.assertEqual(forty_niners.away, "Miami Dolphins")
        self.assertEqual(forty_niners.gameday, "2026-09-20")

    def test_bye_teams_are_those_without_a_game(self):
        from pollofpolls import games, teams as teams_mod

        slate = games.parse_nflverse_games(self.NFLVERSE_SAMPLE, season=2026, week=2)
        resting = games.remaining_bye_teams(sorted(teams_mod.TEAMS), slate)
        self.assertIn("Seattle Seahawks", resting)
        self.assertNotIn("Buffalo Bills", resting)
        self.assertEqual(len(resting), 32 - 8)  # 4 games in the sample


class TestLogoNormalisation(unittest.TestCase):
    """The logo tool is part of the build; its failure modes were all visible
    artifacts on the published page, so they are pinned here."""

    def setUp(self):
        import importlib.util
        import pathlib

        path = pathlib.Path(__file__).resolve().parents[1] / "tools" / "normalize_logos.py"
        spec = importlib.util.spec_from_file_location("normalize_logos", path)
        self.tool = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.tool)

    def test_canvas_plate_is_stripped(self):
        svg = (
            '<svg width="500" height="500"><g fill="none">'
            '<path d="M0 0h500v500H0z"/><path fill="#fff" d="M10 10h20v20H10z"/>'
            "</g></svg>"
        )
        cleaned, removed = self.tool.strip_canvas_plates(svg)
        self.assertEqual(removed, 1)
        self.assertNotIn("M0 0h500v500H0z", cleaned)
        self.assertIn("M10 10h20v20H10z", cleaned)

    def test_frame_never_hugs_the_artwork(self):
        # A mark that fills its whole canvas must still get a larger frame, or
        # white artwork touching the edge shows a square seam on the badge.
        full = (0, 0, 499, 499)
        x, y, side = self.tool.square_viewbox(full)
        self.assertGreater(side, 500)
        self.assertLessEqual(x, 0)
        self.assertLessEqual(y, 0)

    def test_frame_is_square_and_centred(self):
        bounds = (60, 20, 440, 300)
        x, y, side = self.tool.square_viewbox(bounds)
        self.assertAlmostEqual(side, 500, places=6)  # padded floor is the canvas
        self.assertAlmostEqual((x + side / 2), (60 + 441) / 2, places=6)
        self.assertAlmostEqual((y + side / 2), (20 + 301) / 2, places=6)

    def test_rewrite_viewbox_replaces_existing(self):
        svg = '<svg width="500" height="500" viewBox="0 0 10 10"><path d="M0 0h1v1H0z"/></svg>'
        out = self.tool.rewrite_viewbox(svg, -1.0, -2.0, 504.0)
        self.assertIn('viewBox="-1 -2 504 504"', out)
        self.assertEqual(out.count("viewBox"), 1)

    def test_rewrite_viewbox_inserts_when_missing(self):
        svg = '<svg width="500" height="500"><path d="M0 0h1v1H0z"/></svg>'
        out = self.tool.rewrite_viewbox(svg, 0.0, 0.0, 500.0)
        self.assertIn('viewBox="0 0 500 500"', out)


if __name__ == "__main__":
    unittest.main(verbosity=2)
