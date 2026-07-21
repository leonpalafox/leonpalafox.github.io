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
    source: z.string().url().optional(),
  }),
});

export const collections = { blog };
