"""The 12 Express Lines — original roadmaps built on free, reputable resources."""

KA = "https://www.khanacademy.org"
LINES = [
 {
  "slug": "ai", "short": "AI & Prompting", "code": "AI", "name": "AI & Prompting Line", "color": "#6D28D9", "cat": "ai", "hours": 24,
  "tag": "Use AI tools confidently at work and in study — no math degree required.",
  "intro": [
   "Artificial intelligence moved from research labs into everyday software in just a few years. Employers no longer ask whether you have heard of AI; they ask whether you can use it to work faster without making costly mistakes. This line gets you there in about 24 focused hours.",
   "You will start with intuition — what a model actually does when it \"predicts the next word\" — then move to practical prompting, evaluating output, and building small automations. The final station introduces the core machine-learning ideas so you can keep going toward technical roles if you want to."
  ],
  "for": "Students, office professionals, creators and career-switchers.",
  "outcome": "A personal prompt library, three automated workflows and the vocabulary to talk about AI with technical teams.",
  "stations": [
   ("What AI really is (and isn't)", 3, "Learn the difference between traditional software, machine learning and large language models. Understand training data, why models hallucinate, and why confident output is not the same as correct output.", [("Elements of AI (free course)", "https://www.elementsofai.com/"), ("3Blue1Brown: Neural networks", "https://www.3blue1brown.com/topics/neural-networks")]),
   ("Prompting fundamentals", 4, "Practise the five-part prompt: role, task, context, constraints and output format. Rewrite one vague prompt five times and compare the answers side by side to see what each part changes.", [("Google Prompting Essentials overview", "https://grow.google/prompting-essentials/"), ("Learn Prompting (open guide)", "https://learnprompting.org/docs/introduction")]),
   ("Checking AI output", 3, "Build a verification habit: ask for sources, cross-check numbers, test code before trusting it, and never paste private or client data into public tools. Create a one-page checklist you will reuse.", [("NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework")]),
   ("AI for writing, research & study", 4, "Use AI as a tutor rather than a ghost-writer: generate practice questions, explain a concept three ways, summarise a reading and then quiz yourself without the summary.", [("Our guide: Learning with AI", "guide-learn-with-ai.html"), ("Khan Academy: AI for education", f"{KA}/college-careers-more/ai-for-education")]),
   ("No-code automations", 5, "Connect a form, a spreadsheet and an AI step to remove one repetitive task from your week. Document the before-and-after time saved — it is the most persuasive line on a CV.", [("Microsoft Learn: AI skills", "https://learn.microsoft.com/en-us/training/topics/ai-skills"), ("Google Apps Script basics", "https://developers.google.com/apps-script/overview")]),
   ("Machine-learning foundations", 5, "Meet supervised learning, training vs. test data, overfitting and evaluation metrics through hands-on notebooks. This is your on-ramp if you want to become technical.", [("Google ML Crash Course", "https://developers.google.com/machine-learning/crash-course"), ("Kaggle Learn: Intro to ML", "https://www.kaggle.com/learn/intro-to-machine-learning")]),
  ],
  "faq": [("Do I need coding for this line?", "No. Stations 1–5 are code-free. Station 6 uses simple Python notebooks that run in the browser."), ("Which AI tool should I use?", "Any mainstream assistant works. The skills — clear prompts and careful verification — transfer between tools.")],
  "yt": "AI tutorial for beginners",
 },
 {
  "slug": "web", "short": "Coding & Web", "code": "WEB", "name": "Coding & Web Dev Line", "color": "#1F5BFF", "cat": "web", "hours": 120,
  "tag": "From your first HTML tag to a deployed portfolio project.",
  "intro": [
   "Web development remains one of the most accessible paths into tech because everything you need is free: a browser, a text editor and the open web. What most beginners lack is not material but order. This line gives you the order.",
   "Follow the stations in sequence and build something at every stop. By the end you will have a responsive portfolio site, a JavaScript app that talks to a real API and a public code history that shows employers how you think."
  ],
  "for": "Absolute beginners and self-taught coders who keep restarting tutorials.",
  "outcome": "A deployed portfolio, two JavaScript projects and a GitHub profile with regular commits.",
  "stations": [
   ("HTML: structure", 10, "Learn semantic tags, headings, links, images, forms and accessibility basics. Build a single-page profile with valid, well-structured markup.", [("MDN Learn web development", "https://developer.mozilla.org/en-US/docs/Learn"), ("freeCodeCamp curriculum", "https://www.freecodecamp.org/learn")]),
   ("CSS: layout & responsive design", 15, "Master the box model, Flexbox, Grid and media queries. Rebuild your profile so it looks great from a phone to a wide monitor.", [("web.dev Learn CSS", "https://web.dev/learn/css"), ("W3Schools CSS", "https://www.w3schools.com/css/")]),
   ("JavaScript fundamentals", 30, "Variables, functions, arrays, objects, loops and the DOM. Make your page interactive with a theme switcher, a form validator and a to-do list.", [("javascript.info", "https://javascript.info/"), ("freeCodeCamp JavaScript", "https://www.freecodecamp.org/learn")]),
   ("Git & GitHub", 6, "Version control is non-negotiable on a team. Learn commits, branches and pull requests, then publish your site for free with GitHub Pages.", [("GitHub Skills", "https://skills.github.com/"), ("Pro Git book", "https://git-scm.com/book/en/v2")]),
   ("APIs & async JavaScript", 20, "Fetch real data, handle loading and errors, and build a weather or book-search app. This is where tutorials end and engineering begins.", [("MDN: Using Fetch", "https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch"), ("Public APIs list", "https://github.com/public-apis/public-apis")]),
   ("Full curriculum & computer science", 39, "Go deeper with a complete open curriculum and a university-grade intro to computer science. Pick one and finish it.", [("The Odin Project", "https://www.theodinproject.com/paths"), ("Harvard CS50x", "https://cs50.harvard.edu/x/")]),
  ],
  "faq": [("How long until I'm job-ready?", "Most self-taught developers need 6–12 months of consistent practice beyond this line. Use Program Match if you want a structured bootcamp with career support."), ("Which language first?", "JavaScript, because it runs in every browser and lets you see results instantly.")],
  "yt": "web development full course beginners",
 },
 {
  "slug": "data", "short": "Data & SQL", "code": "DATA", "name": "Data, Excel & SQL Line", "color": "#0EA5A4", "cat": "data", "hours": 60,
  "tag": "Turn spreadsheets into decisions with formulas, SQL and clear charts.",
  "intro": [
   "Every organisation runs on data, yet most of it sits in spreadsheets that nobody fully understands. People who can clean, query and explain that data become indispensable quickly — often without a computer-science degree.",
   "This line moves from spreadsheet confidence to SQL, statistics and storytelling with charts. Each station ends with a mini-project using a real public dataset so you leave with a portfolio, not just notes."
  ],
  "for": "Analysts-in-training, admin and operations staff, students and small-business owners.",
  "outcome": "Three portfolio analyses, working SQL skills and a dashboard you can show in interviews.",
  "stations": [
   ("Spreadsheet power skills", 10, "Cell references, lookups, pivot tables, conditional formatting and data validation. Rebuild a messy budget into a clean, auditable model.", [("Microsoft Excel help & learning", "https://support.microsoft.com/en-us/excel"), ("Google Sheets training", "https://support.google.com/a/users/answer/9282959")]),
   ("Cleaning data", 8, "Handle duplicates, inconsistent dates, blanks and outliers. Write down every cleaning step so someone else could repeat your work exactly.", [("Kaggle Learn: Data Cleaning", "https://www.kaggle.com/learn/data-cleaning")]),
   ("SQL fundamentals", 12, "SELECT, WHERE, GROUP BY, JOIN and subqueries. Practise in the browser until joins feel natural.", [("SQLBolt interactive lessons", "https://sqlbolt.com/"), ("Kaggle Learn: Intro to SQL", "https://www.kaggle.com/learn/intro-to-sql")]),
   ("Statistics you will actually use", 12, "Averages vs. medians, spread, sampling, correlation vs. causation and A/B tests. Learn to say how confident you are, not just what the number is.", [("Khan Academy Statistics", f"{KA}/math/statistics-probability"), ("OpenStax Introductory Statistics", "https://openstax.org/details/books/introductory-statistics-2e")]),
   ("Charts & storytelling", 8, "Choose the right chart, remove clutter and write a headline that states the insight. Present one analysis in five slides or fewer.", [("Data Visualization Catalogue", "https://datavizcatalogue.com/")]),
   ("Python for analysis", 10, "Use pandas to load, clean and summarise data in notebooks — the bridge to data-science roles.", [("Kaggle Learn: Pandas", "https://www.kaggle.com/learn/pandas"), ("freeCodeCamp Data Analysis", "https://www.freecodecamp.org/learn")]),
  ],
  "faq": [("Excel or Google Sheets?", "Either. The concepts are nearly identical; employers care that you can model and explain data."), ("Is SQL hard?", "Basic SQL is one of the fastest technical skills to learn — most people write useful queries within a week.")],
  "yt": "excel sql data analysis tutorial",
 },
 {
  "slug": "marketing", "short": "Marketing", "code": "MKT", "name": "Digital Marketing Line", "color": "#FF5A1F", "cat": "mkt", "hours": 40,
  "tag": "SEO, content, social and analytics — the skills every business pays for.",
  "intro": [
   "Digital marketing is measurable, which makes it one of the easiest fields to prove your value in. Whether you want a marketing job, freelance clients or customers for your own product, the same core skills apply: understand the audience, create something useful and measure what happens.",
   "This line is built around free, industry-issued training and practical exercises you can run on a personal blog or a friend's small business."
  ],
  "for": "Freelancers, small-business owners, creators and marketing beginners.",
  "outcome": "A live content project with tracked results and two recognised free certificates.",
  "stations": [
   ("Marketing foundations", 5, "Positioning, audiences, the customer journey and the difference between brand and performance marketing.", [("HubSpot Academy", "https://academy.hubspot.com/"), ("Google Skillshop", "https://skillshop.withgoogle.com/")]),
   ("Search engine optimisation", 8, "How search engines crawl and rank, keyword intent, on-page structure and why helpful content beats tricks.", [("Google Search Central: SEO Starter Guide", "https://developers.google.com/search/docs/fundamentals/seo-starter-guide")]),
   ("Content that earns attention", 7, "Write headlines, outlines and articles that answer real questions. Publish three pieces and track their performance.", [("Our guide: The Express Method", "guide-express-method.html")]),
   ("Social media & community", 6, "Choose one platform where your audience already spends time, plan a 30-day calendar and learn which metrics matter.", [("Meta Blueprint", "https://www.facebook.com/business/learn")]),
   ("Email marketing", 6, "Lead magnets, welcome sequences and segmentation — the channel with consistently strong returns.", [("HubSpot Academy: Email Marketing", "https://academy.hubspot.com/courses/email-marketing")]),
   ("Analytics & reporting", 8, "Set up analytics, define conversions and build a monthly report that leads to decisions, not just charts.", [("Google Analytics Academy on Skillshop", "https://skillshop.withgoogle.com/")]),
  ],
  "faq": [("Are free marketing certificates respected?", "Industry-issued certificates show initiative; a live project with real numbers shows ability. Get both."), ("Do I need a budget?", "No. Every station can be practised with organic content.")],
  "yt": "digital marketing course for beginners",
 },
 {
  "slug": "finance", "short": "Finance", "code": "FIN", "name": "Personal Finance & Investing Line", "color": "#14A44D", "cat": "fin", "hours": 18,
  "tag": "Budget, borrow, save and invest with clear rules of thumb.",
  "intro": [
   "Money skills compound. A few hours learning how interest, taxes and diversification work can change decades of outcomes — yet most people were never taught. This line covers the essentials in plain language.",
   "It is educational, not personalised advice. Rules and products differ by country, so each station points to official consumer-protection resources you can trust."
  ],
  "for": "Students, first-job earners, families and anyone starting over financially.",
  "outcome": "A working budget, a debt-payoff plan and a written investing policy you understand.",
  "stations": [
   ("Budgeting that sticks", 3, "Track one month of spending, then build a simple needs-wants-goals budget. Automate savings on payday.", [("CFPB consumer tools", "https://www.consumerfinance.gov/consumer-tools/"), ("Khan Academy Personal Finance", f"{KA}/college-careers-more/personal-finance")]),
   ("Debt & credit", 3, "How interest really accrues, avalanche vs. snowball payoff, and what moves a credit score.", [("CFPB: Credit reports and scores", "https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/")]),
   ("Emergency fund & insurance", 2, "Size an emergency fund, understand deductibles and premiums, and protect against the risks that cause most financial setbacks.", [("Investor.gov: Saving and investing", "https://www.investor.gov/introduction-investing")]),
   ("How investing works", 4, "Stocks, bonds, funds, fees and diversification. Why low-cost broad index funds are a common starting point, and what risk really means.", [("Investor.gov basics", "https://www.investor.gov/introduction-investing/investing-basics"), ("Bogleheads wiki", "https://www.bogleheads.org/wiki/Main_Page")]),
   ("Tax-advantaged accounts", 3, "Learn the purpose of retirement and education accounts in your country and how employer matching works.", [("Canada.ca: TFSA", "https://www.canada.ca/en/revenue-agency/services/tax/individuals/topics/tax-free-savings-account.html"), ("IRS: Retirement plans", "https://www.irs.gov/retirement-plans")]),
   ("Avoiding scams", 3, "Recognise guaranteed-return pitches, pressure tactics and fake platforms. Learn to verify any adviser or firm before sending money.", [("Investor.gov: Protect your investments", "https://www.investor.gov/protect-your-investments")]),
  ],
  "faq": [("Is this financial advice?", "No. It is general education. For decisions about your situation, consult a licensed professional."), ("Where do I start if I have debt?", "Stations 1 and 2 — a budget and a payoff plan come before investing.")],
  "yt": "personal finance basics",
 },
 {
  "slug": "languages", "short": "Languages", "code": "LANG", "name": "Language Learning Line", "color": "#E11D74", "cat": "lang", "hours": 90,
  "tag": "Reach conversational level with daily input, spaced review and real speaking.",
  "intro": [
   "Languages are learned through massive comprehensible input — listening and reading material you mostly understand — combined with regular speaking practice. Apps are a good start, but they are only one part of the system.",
   "This line gives you a 90-hour framework that works for any language: build a core vocabulary, absorb native content, review with spaced repetition and speak early, even imperfectly."
  ],
  "for": "Travellers, newcomers, heritage speakers and exam candidates.",
  "outcome": "1,000+ core words, a daily listening habit and your first 10 real conversations.",
  "stations": [
   ("Sounds & survival phrases", 8, "Learn the sound system and 100 phrases you will use every day. Record yourself and compare with native audio.", [("Forvo pronunciation dictionary", "https://forvo.com/"), ("Language Transfer (free audio)", "https://www.languagetransfer.org/")]),
   ("Core vocabulary with spaced repetition", 20, "Learn the 1,000 most frequent words using flashcards that schedule reviews right before you would forget.", [("Anki flashcards", "https://apps.ankiweb.net/"), ("Our Flashcard tool", "tools.html#flash")]),
   ("Daily app practice", 15, "Use one app for 15 minutes daily to keep momentum — treat it as warm-up, not the whole workout.", [("Duolingo", "https://www.duolingo.com/"), ("Memrise", "https://www.memrise.com/")]),
   ("Comprehensible input", 25, "Watch beginner-friendly video and graded readers. Aim for content where you understand at least 70%.", [("YouTube: comprehensible input", "https://www.youtube.com/results?search_query=comprehensible+input+beginner")]),
   ("Grammar as a map", 10, "Study grammar to understand patterns you have already heard, not as a list of rules to memorise first.", [("OpenStax / open textbooks", "https://open.umn.edu/opentextbooks/subjects/languages")]),
   ("Speaking & feedback", 12, "Book conversation exchanges or tutors. Keep a mistake journal and recycle errors into flashcards.", [("Tandem language exchange", "https://www.tandem.net/"), ("italki tutors", "https://www.italki.com/")]),
  ],
  "faq": [("How long to become conversational?", "It depends heavily on the language and your native tongue, but many learners reach basic conversations after 100–200 hours of mixed practice."), ("Can I learn two at once?", "It is possible but slower. Build one to a comfortable level first.")],
  "yt": "comprehensible input beginner",
 },
 {
  "slug": "business", "short": "Business", "code": "BIZ", "name": "Business & Entrepreneurship Line", "color": "#F59E0B", "cat": "biz", "hours": 36,
  "tag": "Validate an idea, find customers and run the numbers before you spend.",
  "intro": [
   "Most new businesses fail for predictable reasons: no real customer demand, unclear pricing or running out of cash. The good news is that each of those risks can be tested cheaply before you commit.",
   "This line walks you from idea to first paying customer using the same lean methods taught in startup accelerators and small-business centres — all available free."
  ],
  "for": "Side-hustlers, freelancers, founders and small-business owners.",
  "outcome": "A validated offer, a one-page business plan and a simple financial model.",
  "stations": [
   ("Find a problem worth solving", 5, "Interview ten potential customers. Listen for frequent, painful, already-paid-for problems.", [("Y Combinator Startup School", "https://www.startupschool.org/")]),
   ("Validate before you build", 6, "Run a landing-page or pre-order test. Define in advance what result counts as success.", [("SBA Learning Platform", "https://www.sba.gov/sba-learning-platform")]),
   ("Pricing & unit economics", 6, "Calculate margin, customer acquisition cost and break-even. Price on value, not just cost.", [("Khan Academy: Entrepreneurship", f"{KA}/college-careers-more/entrepreneurship2")]),
   ("Getting customers", 7, "Pick one acquisition channel and master it before adding another.", [("Digital Marketing Line", "path-marketing.html")]),
   ("Operations & legal basics", 6, "Business structures, registration, contracts, invoicing and bookkeeping basics for your region.", [("Canada Business Network", "https://innovation.ised-isde.canada.ca/s/?language=en_CA"), ("SBA: Plan your business", "https://www.sba.gov/business-guide/plan-your-business")]),
   ("Growth & funding options", 6, "Bootstrapping, grants, loans and investors — what each costs you in money and control.", [("SBA: Fund your business", "https://www.sba.gov/business-guide/plan-your-business/fund-your-business")]),
  ],
  "faq": [("Do I need a business plan?", "Start with a one-page plan. Expand it when a lender or investor asks."), ("What is the fastest validation test?", "Asking people to pay — a deposit or pre-order — beats any survey.")],
  "yt": "how to start a business validation",
 },
 {
  "slug": "career", "short": "Career Launch", "code": "JOB", "name": "Career Launch & Interview Line", "color": "#475569", "cat": "job", "hours": 20,
  "tag": "Pick a direction, build proof and win the interview.",
  "intro": [
   "Getting hired is a skill in its own right, separate from being good at the job. Strong candidates research the role, show evidence of results and practise answering questions out loud.",
   "This line takes about 20 hours and pairs naturally with any skill line on this site: learn the skill there, then package and present it here."
  ],
  "for": "Graduates, career-switchers, returners and newcomers to a country.",
  "outcome": "A targeted CV, a portfolio page and ten practised interview stories.",
  "stations": [
   ("Explore careers with data", 3, "Compare duties, pay ranges, education requirements and outlook for roles that interest you.", [("O*NET OnLine", "https://www.onetonline.org/"), ("BLS Occupational Outlook Handbook", "https://www.bls.gov/ooh/"), ("Job Bank Canada", "https://www.jobbank.gc.ca/")]),
   ("Skills gap plan", 3, "List the skills that appear in 10 job ads and map each to a free resource or Express Line.", [("All Express Lines", "paths.html")]),
   ("CV that gets read", 4, "Achievement bullets (action + result + number), tailored keywords and a clean one-column layout.", [("Our Career Switch Roadmap", "guide-career-switch.html")]),
   ("Portfolio & proof", 4, "Publish two or three small case studies that show your process and results.", [("GitHub Pages (free hosting)", "https://pages.github.com/")]),
   ("Interview practice", 4, "Prepare STAR stories, practise out loud and record yourself.", [("Google Interview Warmup", "https://grow.google/certificates/interview-warmup/")]),
   ("Networking & negotiation", 2, "Write short, specific outreach messages and learn to negotiate respectfully with market data.", [("BLS pay data", "https://www.bls.gov/oes/")]),
  ],
  "faq": [("How many applications should I send?", "Fewer, better-targeted applications with a referral or tailored CV outperform mass applying."), ("Do I need a certificate to switch careers?", "Sometimes. Use Program Match to compare certificate, bootcamp and degree options for your goal.")],
  "yt": "job interview tips STAR method",
 },
 {
  "slug": "study-skills", "short": "Study Skills", "code": "STDY", "name": "Study Skills Line", "color": "#C026D3", "cat": "study", "hours": 10,
  "tag": "Learn how to learn — the multiplier for every other line.",
  "intro": [
   "Re-reading and highlighting feel productive but are among the least effective study methods. Decades of cognitive-science research point to a short list of techniques that work far better: retrieval practice, spacing, interleaving and elaboration.",
   "This is the shortest line on the network and the one we recommend everyone rides first. Ten hours here make every future hour of study more effective."
  ],
  "for": "Everyone — especially exam candidates and adult learners returning to study.",
  "outcome": "A personal study system you can apply to any subject.",
  "stations": [
   ("How memory works", 1, "Encoding, consolidation, retrieval and why forgetting is part of learning.", [("Learning How to Learn (Coursera, free to audit)", "https://www.coursera.org/learn/learning-how-to-learn")]),
   ("Active recall", 2, "Close the book and write what you remember. Turn every heading into a question.", [("Our guide: Active Recall", "guide-active-recall.html")]),
   ("Spaced repetition", 2, "Review at expanding intervals instead of cramming.", [("Our guide: Spaced Repetition", "guide-spaced-repetition.html"), ("Flashcard tool", "tools.html#flash")]),
   ("Focus & time blocks", 2, "Use Pomodoro sprints, remove phone distractions and protect one deep-work block daily.", [("Our guide: Pomodoro & Deep Focus", "guide-pomodoro-focus.html"), ("Focus Timer", "tools.html#timer")]),
   ("Explain it simply", 1, "Use the Feynman technique to expose gaps in understanding.", [("Our guide: Feynman Technique", "guide-feynman-technique.html")]),
   ("Plan the week", 2, "Build a weekly plan that survives real life, with review days built in.", [("Our guide: Weekly Study Plan", "guide-study-plan.html"), ("30-Day Planner", "planner.html")]),
  ],
  "faq": [("Is highlighting useless?", "Not useless, but weak on its own. Pair it with self-testing."), ("How long should a study session be?", "25–50 minutes of focused work followed by a short break suits most people.")],
  "yt": "how to study effectively active recall",
 },
 {
  "slug": "math", "short": "Math", "code": "MATH", "name": "Math Foundations Line", "color": "#DC2626", "cat": "math", "hours": 80,
  "tag": "Arithmetic to algebra and statistics — rebuild confidence step by step.",
  "intro": [
   "Many adults believe they are \"not a math person\" when they simply missed a foundation years ago. Mathematics is cumulative: fix the missing layer and everything above it becomes easier.",
   "This line uses free mastery-based practice so you can find your real starting point, close gaps and progress to the algebra and statistics needed for college, trades and technical careers."
  ],
  "for": "Returning students, college-placement candidates, parents and tradespeople.",
  "outcome": "Algebra fluency, statistics basics and the ability to tackle quantitative courses.",
  "stations": [
   ("Find your level", 2, "Take a diagnostic and start one level below where you feel comfortable.", [("Khan Academy Math", f"{KA}/math")]),
   ("Numbers, fractions & percent", 15, "Fractions, decimals, ratios and percentages — the everyday math behind finance, recipes and measurements.", [("Khan Academy Arithmetic", f"{KA}/math/arithmetic"), ("Math is Fun", "https://www.mathsisfun.com/")]),
   ("Pre-algebra", 15, "Negative numbers, order of operations, exponents and simple equations.", [("Khan Academy Pre-algebra", f"{KA}/math/pre-algebra")]),
   ("Algebra I", 25, "Linear equations, inequalities, functions and graphs. Use a graphing calculator to see what equations mean.", [("Khan Academy Algebra 1", f"{KA}/math/algebra"), ("Desmos graphing calculator", "https://www.desmos.com/calculator")]),
   ("Geometry & measurement", 10, "Area, volume, angles, the Pythagorean theorem and unit conversion.", [("Khan Academy Geometry", f"{KA}/math/geometry")]),
   ("Statistics & probability", 13, "Data displays, averages, spread and basic probability.", [("OpenStax Introductory Statistics", "https://openstax.org/details/books/introductory-statistics-2e"), ("Paul's Online Math Notes", "https://tutorial.math.lamar.edu/")]),
  ],
  "faq": [("I'm years out of school. Where do I start?", "Take the diagnostic in Station 1 — most people are pleasantly surprised."), ("Can I use a calculator?", "Yes for checking, but practise by hand until the method is automatic.")],
  "yt": "algebra basics for beginners",
 },
 {
  "slug": "science", "short": "Science", "code": "SCI", "name": "Science Essentials Line", "color": "#0891B2", "cat": "sci", "hours": 60,
  "tag": "Biology, chemistry and physics explained with simulations and stories.",
  "intro": [
   "Science literacy helps you evaluate health claims, understand the news and prepare for college or technical training. You do not need a lab — free interactive simulations and university-level open textbooks bring the concepts to life.",
   "This line covers the big ideas of the three core sciences and finishes with how to read a scientific study critically."
  ],
  "for": "High-school and college students, homeschool families and curious adults.",
  "outcome": "Working knowledge of core scientific concepts and the ability to judge evidence.",
  "stations": [
   ("The scientific method", 3, "Hypotheses, controls, variables and why replication matters.", [("Khan Academy Biology: intro", f"{KA}/science/biology")]),
   ("Biology: life's machinery", 15, "Cells, DNA, evolution and human body systems.", [("OpenStax Biology 2e", "https://openstax.org/details/books/biology-2e"), ("Khan Academy Biology", f"{KA}/science/biology")]),
   ("Chemistry: matter & reactions", 14, "Atoms, the periodic table, bonding and reactions.", [("OpenStax Chemistry 2e", "https://openstax.org/details/books/chemistry-2e"), ("PhET chemistry simulations", "https://phet.colorado.edu/en/simulations/filter?subjects=chemistry")]),
   ("Physics: forces & energy", 15, "Motion, forces, energy, waves and electricity with interactive simulations.", [("PhET physics simulations", "https://phet.colorado.edu/en/simulations/filter?subjects=physics"), ("Khan Academy Physics", f"{KA}/science/physics")]),
   ("Earth & space", 8, "Climate systems, geology and the solar system.", [("NASA learning resources", "https://www.nasa.gov/learning-resources/")]),
   ("Reading a study", 5, "Sample sizes, correlation vs. causation, peer review and how to spot misleading headlines.", [("Understanding Science (UC Berkeley)", "https://undsci.berkeley.edu/")]),
  ],
  "faq": [("Which science should I start with?", "Biology is the most intuitive entry point; physics benefits from the Math line first."), ("Are open textbooks rigorous?", "Yes. OpenStax books are peer-reviewed and used in many colleges.")],
  "yt": "crash course biology chemistry physics",
 },
 {
  "slug": "health-careers", "short": "Health Careers", "code": "CARE", "name": "Health & Care Careers Line", "color": "#65A30D", "cat": "care", "hours": 40,
  "tag": "Explore healthcare roles and build the science foundation they require.",
  "intro": [
   "Healthcare offers some of the most stable and meaningful careers available, from personal support work and pharmacy technicians to nursing and medical imaging. Each path has different entry requirements, timelines and costs.",
   "This line helps you compare roles with official labour data, build the anatomy and terminology foundation most programs expect, and prepare to choose an accredited program. It is career education, not clinical advice."
  ],
  "for": "Career-switchers, high-school students and caregivers considering formal training.",
  "outcome": "A shortlist of suitable roles, foundation knowledge and a program-selection checklist.",
  "stations": [
   ("Map the roles", 4, "Compare duties, schooling, licensing and pay for 10 healthcare occupations.", [("BLS Healthcare occupations", "https://www.bls.gov/ooh/healthcare/home.htm"), ("Job Bank Canada: explore careers", "https://www.jobbank.gc.ca/")]),
   ("Medical terminology", 8, "Roots, prefixes and suffixes that unlock thousands of medical words.", [("MedlinePlus: Understanding medical words", "https://medlineplus.gov/medicalwords.html")]),
   ("Anatomy & physiology", 15, "Body systems and how they work together.", [("OpenStax Anatomy & Physiology 2e", "https://openstax.org/details/books/anatomy-and-physiology-2e"), ("Khan Academy Health & Medicine", f"{KA}/science/health-and-medicine")]),
   ("Health literacy & safety", 5, "Infection prevention, patient privacy principles and reliable health information sources.", [("MedlinePlus", "https://medlineplus.gov/"), ("WHO: Infection prevention", "https://www.who.int/teams/integrated-health-services/infection-prevention-control")]),
   ("Choose an accredited program", 4, "Check accreditation, clinical placement support, licensing pass rates and total cost.", [("Our guide: Choosing an Online Program", "guide-choose-online-program.html"), ("Program Match", "match.html")]),
   ("Prepare to apply", 4, "Prerequisites, references, volunteering and admissions interviews.", [("Career Launch Line", "path-career.html")]),
  ],
  "faq": [("Can I train fully online?", "Theory often can be online, but most licensed roles require supervised clinical hours in person."), ("Which roles have the shortest training?", "Support and technician roles often take months rather than years — compare them in Station 1.")],
  "yt": "anatomy and physiology basics",
 },
]
