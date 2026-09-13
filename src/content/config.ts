import { defineCollection, z } from 'astro:content';

const landingpages = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    metaTitle: z.string().optional(),
    metaDescription: z.string(),
    keyword: z.string(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { landingpages };
