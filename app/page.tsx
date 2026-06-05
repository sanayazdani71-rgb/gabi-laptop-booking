// Replace GUMROAD_LINK with your actual Gumroad product URL before launch
const GUMROAD_LINK = 'https://gumroad.com/l/YOUR_PRODUCT_SLUG'

const INCLUDES = [
  { emoji: '💧', label: 'Daily habit tracker', detail: '30 days, pre-structured' },
  { emoji: '🏋️', label: 'Workout planner', detail: 'Weekly schedule + log' },
  { emoji: '✨', label: 'Skin-care routine tracker', detail: 'AM & PM routines' },
  { emoji: '📏', label: 'Body measurements log', detail: 'Weight, waist, progress' },
  { emoji: '📝', label: 'Weekly reflection pages', detail: 'Guided prompts' },
  { emoji: '🌟', label: 'Motivation & vision pages', detail: 'Start strong, stay strong' },
]

const FAQS = [
  {
    q: 'What format does this come in?',
    a: 'You get a Notion template you duplicate into your own workspace in one click. Works on desktop and mobile.',
  },
  {
    q: 'Do I need a paid Notion plan?',
    a: 'No. The free Notion plan is enough to use everything inside.',
  },
  {
    q: 'Is this a course or coaching?',
    a: 'Neither. It is a ready-made system — you fill it in, the structure does the work.',
  },
  {
    q: 'What if it is not right for me?',
    a: 'If you buy it and feel it is not worth it, email me and I will refund you. No questions asked.',
  },
]

export default function Page() {
  return (
    <main className="min-h-screen" style={{ fontFamily: 'Inter, system-ui, sans-serif', backgroundColor: '#FAF7F2', color: '#2C2C2C' }}>

      {/* NAV */}
      <nav className="flex items-center justify-between px-6 py-5 max-w-4xl mx-auto">
        <span className="text-sm font-medium tracking-widest uppercase" style={{ color: '#8B6F5E' }}>
          Life Design
        </span>
        <a
          href={GUMROAD_LINK}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-medium px-5 py-2 rounded-full transition-opacity hover:opacity-80"
          style={{ backgroundColor: '#2C2C2C', color: '#FAF7F2' }}
        >
          Get the template — €19
        </a>
      </nav>

      {/* HERO */}
      <section className="max-w-3xl mx-auto px-6 pt-16 pb-20 text-center">
        <p className="text-xs tracking-widest uppercase mb-6" style={{ color: '#A8B5A0' }}>
          Notion template · instant download
        </p>
        <h1
          className="text-4xl sm:text-6xl leading-tight mb-6"
          style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}
        >
          The 30-Day<br />
          <em>Glow-Up</em> System
        </h1>
        <p className="text-lg leading-relaxed mb-10 max-w-xl mx-auto" style={{ color: '#5C5C5C' }}>
          Everything is already built. You just fill it in.
          Your habits, your workouts, your skin-care, your reflection — all in one place, for 30 days.
        </p>
        <a
          href={GUMROAD_LINK}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block text-base font-medium px-10 py-4 rounded-full transition-opacity hover:opacity-80"
          style={{ backgroundColor: '#2C2C2C', color: '#FAF7F2' }}
        >
          Get instant access — €19
        </a>
        <p className="mt-4 text-sm" style={{ color: '#A8B5A0' }}>
          One-time payment · no subscription · refund if not satisfied
        </p>
      </section>

      {/* DIVIDER */}
      <div className="max-w-4xl mx-auto px-6">
        <div style={{ height: '1px', backgroundColor: '#E8E0D5' }} />
      </div>

      {/* THE REAL PROBLEM */}
      <section className="max-w-2xl mx-auto px-6 py-20 text-center">
        <h2 className="text-2xl sm:text-3xl mb-6" style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}>
          You already know what to do.
        </h2>
        <p className="text-lg leading-relaxed" style={{ color: '#5C5C5C' }}>
          Drink more water. Move your body. Sleep. Reflect. Save money.
        </p>
        <p className="text-lg leading-relaxed mt-4" style={{ color: '#5C5C5C' }}>
          The problem is not knowledge. The problem is that without a system,
          good intentions disappear by day three.
        </p>
        <p className="text-lg leading-relaxed mt-4 font-medium" style={{ color: '#2C2C2C' }}>
          This template is the system.
        </p>
      </section>

      {/* WHAT'S INSIDE */}
      <section className="max-w-4xl mx-auto px-6 pb-20">
        <h2 className="text-2xl sm:text-3xl mb-12 text-center" style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}>
          What is inside
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {INCLUDES.map(({ emoji, label, detail }) => (
            <div
              key={label}
              className="flex items-start gap-4 p-5 rounded-2xl"
              style={{ backgroundColor: '#F2EDE6' }}
            >
              <span className="text-2xl mt-0.5">{emoji}</span>
              <div>
                <p className="font-medium">{label}</p>
                <p className="text-sm mt-0.5" style={{ color: '#8B6F5E' }}>{detail}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* SOCIAL PROOF PLACEHOLDER */}
      <section className="max-w-3xl mx-auto px-6 pb-20">
        <div
          className="rounded-3xl p-10 text-center"
          style={{ backgroundColor: '#F2D4C8' }}
        >
          <p className="text-lg italic leading-relaxed mb-4" style={{ fontFamily: 'Georgia, serif' }}>
            "I have tried so many apps and planners. This is the first one where I actually kept going
            past week one. The structure removes the decision fatigue."
          </p>
          <p className="text-sm font-medium" style={{ color: '#8B6F5E' }}>
            — Early tester, Berlin
          </p>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="max-w-2xl mx-auto px-6 pb-20 text-center">
        <h2 className="text-2xl sm:text-3xl mb-10" style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}>
          Three steps
        </h2>
        <div className="space-y-8">
          {[
            { n: '01', title: 'Buy and duplicate', body: 'After purchase you get a link. Click "Duplicate to my Notion". Takes 10 seconds.' },
            { n: '02', title: 'Spend five minutes on day one', body: 'Fill in your starting measurements and pick your three habits. That is it.' },
            { n: '03', title: 'Open it every morning', body: 'The template tells you exactly what to track. You just tick boxes and fill in numbers.' },
          ].map(({ n, title, body }) => (
            <div key={n} className="flex items-start gap-6 text-left">
              <span
                className="text-3xl font-light flex-shrink-0 w-12"
                style={{ color: '#D4C5B8', fontFamily: 'Georgia, serif' }}
              >
                {n}
              </span>
              <div>
                <p className="font-medium text-lg mb-1">{title}</p>
                <p style={{ color: '#5C5C5C' }}>{body}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA BLOCK */}
      <section
        className="mx-4 sm:mx-auto max-w-3xl rounded-3xl px-8 py-16 mb-16 text-center"
        style={{ backgroundColor: '#2C2C2C', color: '#FAF7F2' }}
      >
        <h2 className="text-3xl sm:text-4xl mb-4" style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}>
          Start your 30 days today.
        </h2>
        <p className="text-base mb-8" style={{ color: '#A8A8A8' }}>
          One template. One month. One version of yourself you have been meaning to become.
        </p>
        <a
          href={GUMROAD_LINK}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block text-base font-medium px-10 py-4 rounded-full transition-opacity hover:opacity-80"
          style={{ backgroundColor: '#FAF7F2', color: '#2C2C2C' }}
        >
          Get the template — €19
        </a>
        <p className="mt-4 text-sm" style={{ color: '#666' }}>
          Instant Notion download · refund if not satisfied
        </p>
      </section>

      {/* FAQ */}
      <section className="max-w-2xl mx-auto px-6 pb-20">
        <h2 className="text-2xl sm:text-3xl mb-10 text-center" style={{ fontFamily: 'Georgia, serif', fontWeight: 400 }}>
          Questions
        </h2>
        <div className="space-y-6">
          {FAQS.map(({ q, a }) => (
            <div key={q} className="border-b pb-6" style={{ borderColor: '#E8E0D5' }}>
              <p className="font-medium mb-2">{q}</p>
              <p style={{ color: '#5C5C5C' }}>{a}</p>
            </div>
          ))}
        </div>
      </section>

      {/* FOOTER */}
      <footer className="border-t py-8 px-6 text-center" style={{ borderColor: '#E8E0D5', color: '#A8A8A8' }}>
        <p className="text-sm">
          Questions? <a href="mailto:hello@example.com" className="underline hover:opacity-80">hello@example.com</a>
        </p>
        <p className="text-xs mt-2">© 2024 Life Design Templates</p>
      </footer>

    </main>
  )
}
