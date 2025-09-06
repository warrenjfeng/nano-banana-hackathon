export interface HairstyleOption {
  id: string;
  name: string;
  description: string;
  prompt: string;
  category: 'men' | 'women' | 'unisex';
}

export const HAIRSTYLE_PRESETS: HairstyleOption[] = [
  // Men's Styles
  {
    id: 'fade-high',
    name: 'High Fade',
    description: 'Short sides with longer top',
    prompt: 'Apply a high fade haircut with very short sides that gradually get longer toward the top, keeping the top section longer and styled',
    category: 'men'
  },
  {
    id: 'fade-mid',
    name: 'Mid Fade',
    description: 'Medium fade with styled top',
    prompt: 'Apply a mid fade haircut with medium-length sides that blend into a longer top section, creating a clean and modern look',
    category: 'men'
  },
  {
    id: 'buzz-cut',
    name: 'Buzz Cut',
    description: 'Uniform short length',
    prompt: 'Apply a buzz cut with uniform short length all around the head, creating a clean and low-maintenance look',
    category: 'men'
  },
  {
    id: 'undercut',
    name: 'Undercut',
    description: 'Short sides, long top',
    prompt: 'Apply an undercut hairstyle with very short or shaved sides and a significantly longer top section that can be styled',
    category: 'men'
  },
  {
    id: 'pompadour',
    name: 'Pompadour',
    description: 'Classic voluminous style',
    prompt: 'Apply a pompadour hairstyle with short sides and a voluminous, swept-back top section that creates height and volume',
    category: 'men'
  },
  {
    id: 'crew-cut',
    name: 'Crew Cut',
    description: 'Short and neat',
    prompt: 'Apply a crew cut with short, neat hair all around, slightly longer on top and tapered on the sides',
    category: 'men'
  },
  {
    id: 'bald',
    name: 'Bald',
    description: 'Completely shaved head',
    prompt: 'Apply a completely bald look by shaving all hair from the head, creating a clean and smooth appearance',
    category: 'men'
  },

  // Women's Styles
  {
    id: 'ponytail',
    name: 'Ponytail',
    description: 'Classic pulled-back style',
    prompt: 'Style the hair into a ponytail, gathering all hair at the back of the head and securing it with a hair tie',
    category: 'women'
  },
  {
    id: 'bob-cut',
    name: 'Bob Cut',
    description: 'Chin-length classic',
    prompt: 'Apply a bob haircut with hair cut to chin length, creating a clean and classic look that frames the face',
    category: 'women'
  },
  {
    id: 'pixie-cut',
    name: 'Pixie Cut',
    description: 'Short and playful',
    prompt: 'Apply a pixie cut with short hair that is styled in a playful and modern way, typically with some length on top',
    category: 'women'
  },
  {
    id: 'long-layers',
    name: 'Long Layers',
    description: 'Layered long hair',
    prompt: 'Apply long layered hair with varying lengths that create movement and volume, typically shoulder-length or longer',
    category: 'women'
  },
  {
    id: 'braids',
    name: 'Braids',
    description: 'Classic braided style',
    prompt: 'Style the hair into braids, creating a classic and elegant look that can be done in various braid styles',
    category: 'women'
  },
  {
    id: 'karen',
    name: 'Karen',
    description: 'Speak to the manager',
    prompt: 'Apply a "Karen" hairstyle with short, layered hair that is often highlighted or bleached, with a distinctive side-swept bang and a slightly choppy, asymmetrical cut',
    category: 'women'
  },

  // Unisex Styles
  {
    id: 'curly',
    name: 'Curly',
    description: 'Natural curls',
    prompt: 'Apply curly hair texture with natural-looking curls that have volume and bounce',
    category: 'unisex'
  },
  {
    id: 'straight',
    name: 'Straight',
    description: 'Sleek and smooth',
    prompt: 'Apply straight hair that is sleek, smooth, and well-groomed',
    category: 'unisex'
  },
  {
    id: 'wavy',
    name: 'Wavy',
    description: 'Natural waves',
    prompt: 'Apply wavy hair texture with natural-looking waves that have movement and body',
    category: 'unisex'
  },
  {
    id: 'afro',
    name: 'Afro',
    description: 'Full and voluminous',
    prompt: 'Apply an afro hairstyle with full, voluminous, and naturally curly hair that creates a rounded shape',
    category: 'unisex'
  },
  {
    id: 'bananas',
    name: '🍌 Bananas',
    description: 'Nano banana hackathon special!',
    prompt: 'Create a whimsical and fun hairstyle using a cornucopia of bright yellow bananas arranged creatively on the head, like a crown or headpiece made entirely of bananas. Make it look playful and festive while maintaining the person\'s facial features.',
    category: 'unisex'
  }
];

export const getHairstyleById = (id: string): HairstyleOption | undefined => {
  return HAIRSTYLE_PRESETS.find(style => style.id === id);
};
