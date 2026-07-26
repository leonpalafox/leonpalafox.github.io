import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    pubDate: z.coerce.date(),
    lang: z.enum(['es', 'en']).default('es'),
    tags: z.array(z.string()).default([]),
    // Where the piece first ran. sourceName is the outlet label; it falls back to the hostname.
    source: z.string().url().optional(),
    sourceName: z.string().optional(),
    // Same piece in the other language, when it lives off-site (Medium, an outlet, etc.).
    translation: z
      .object({
        lang: z.enum(['es', 'en']),
        url: z.string().url(),
        label: z.string().optional(),
      })
      .optional(),
    // Cover art, by asset id from src/assets/blog/ — see src/lib/assets.ts.
    // coverAlt/coverCaption override the registry entry for this post only.
    cover: z.string().optional(),
    coverAlt: z.string().optional(),
    coverCaption: z.string().optional(),
  }),
});

export const collections = { blog };
