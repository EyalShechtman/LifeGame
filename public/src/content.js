export const PLAYERS = [
  { id:'arkero', name:'Arkero', rank:'A', suit:'♠', short:'AI agents and a sponsorship CRM for pro football clubs. My day job.',
    line:'Football clubs still run their business on spreadsheets and group chats. At Arkero we’re replacing them with AI, and I was the second engineer through the door. Want to see my hand?',
    more:'I co-led our AI-native sponsorship CRM from the first customer interviews to 5 live clubs and 2 MLS pilots in three months. I built the agents behind it: 400+ runs per customer a day, with RAG and a custom MCP server, and agents that turn emails and meetings into CRM updates (889 approved, 94% acceptance). I also run the demos and deployments on-site with clubs in Europe.',
    facts:[['Built with','Next.js, TypeScript, Postgres, Trigger.dev, LLM agents, MCP'],['My role','Founding engineer / FDE, since Feb 2026'],['Status','5 live clubs · 2 MLS pilots · $6M seed'],['Link','https://arkero.ai']],
    look:{fur:'#8b5a2b', hat:'#16161a', vest:'#15171d', shirt:'#f7f5f0', pants:'#15171d'} },
  { id:'chewy', name:'Chewy', rank:'K', suit:'♣', short:'Software engineer on the data platform. 3rd of 200 at the internal hackathon.',
    line:'Before Arkero I was a software engineer at Chewy, in Bellevue. I built an agentic Airflow framework that took 3rd of 200 at the company hackathon, and made order imports 30% faster. Want the details?',
    more:'The Airflow framework runs 11 automated workflows that used to be manual, built with ML and BI engineers. I sped up order batch imports by 30%, and built an event pipeline on AWS SNS and SQS, all in Terraform.',
    facts:[['Built with','Python, Apache Airflow, AWS SNS/SQS, Terraform'],['My role','Software Engineer I · Jun 2025 – Feb 2026'],['Hackathon','3rd of 200 · agentic Airflow framework'],['Impact','11 automated workflows · 30% faster imports']],
    look:{fur:'#c9a27a', hat:'#0d2a6b', vest:'#1c49c2', shirt:'#f5f6fa', pants:'#13234a'} },
  { id:'hackathons', name:'Hackathons', rank:'Q', suit:'♥', short:'1st of ~350 (DeepMind × YC), 4th of ~800 (OpenAI), 7th of 300+ (Meta).',
    line:'I’m the weekends. BeamBell took 1st of about 350 at Google DeepMind × YC, Dress2Impress came 4th of about 800 at OpenAI’s GPT-5 hackathon, and OpenStylist was 7th of 300+ at Meta’s. Want to hear how?',
    more:'BeamBell is a fleet of AI phone agents that call around and gather competitive intel, and it won a guaranteed YC interview. Dress2Impress turns your webcam into an avatar, has you shop real clothes against a GPT stylist and walks the look down a generated runway. OpenStylist plans outfits with Gemini and puts you in the real products; its launch post drew 150k views on Reddit and 75 GitHub stars.',
    facts:[['1st of ~350','BeamBell · Google DeepMind × YC · Oct 2025'],['4th of ~800','Dress2Impress · OpenAI GPT-5 · Aug 2025'],['7th of 300+','OpenStylist · Meta · Jun 2025'],['Demo · Dress2Impress','https://youtu.be/s8o59vPj6kY'],['Code · OpenStylist','https://github.com/parsakhaz/open-ai-stylist'],['Link · BeamBell','https://beambell.com']],
    look:{fur:'#d9b48a', hat:'#1d1a14', vest:'#6a4a1a', shirt:'#f7f2e8', pants:'#2a2218'} },
  { id:'pictur', name:'Pictur.ai', rank:'J', suit:'♦', short:'An AI image studio: 45+ tools, built solo.',
    line:'Pictur is my AI image studio: more than 45 tools to remove backgrounds, sharpen photos and generate art, all in one place. I built the whole thing myself. Feeling lucky?',
    more:'Next.js 15 and Supabase on the web, with rate limiting and analytics built in, plus Glimmr, a companion iPhone app written in Swift. It launched in September 2025, has made 1,200+ images for hundreds of users, and I’m still shipping to it.',
    facts:[['Built with','Next.js 15, TypeScript, Supabase, Swift'],['My role','Solo: design, code, launch'],['Reach','1,200+ generations from hundreds of users'],['Link','https://pictur.ai']],
    look:{fur:'#efe9de', hat:'#2a1015', vest:'#5e1626', shirt:'#f6f1e7', pants:'#5e1626'} },
  { id:'panenka', name:'Panenka', rank:'10', suit:'♠', short:'A daily football quiz where every answer is a penalty.',
    line:'A daily football quiz where every answer is a penalty kick. The keeper dives where everyone else answered, so the rarer your right answer, the better your finish. Want to step up?',
    more:'Five prompts a day, 25 seconds each, plus an unlimited mode and live rooms for up to ten friends. It runs on Cloudflare Workers with Durable Objects and WebSockets, the animation is drawn on a canvas, and every sound is synthesized in the browser.',
    facts:[['Built with','React, Cloudflare Workers, Durable Objects'],['My role','Creator'],['Status','Live, new questions every day'],['Link','https://dailypanenka.com']],
    look:{fur:'#8d9096', hat:'#161b26', vest:'#1b2b48', shirt:'#f4f2ee', pants:'#1b2b48'} },
  { id:'blitz', name:'Blitz', rank:'9', suit:'♥', short:'Mass texting and email for student orgs and a city.',
    line:'I co-founded Blitz, a mass texting and email platform. It started as the tool I built to reach my TAMID members, and now student groups and a city government send through it. Interested?',
    more:'Bulk SMS and email that’s simple enough for a club president: contact lists, templates, scheduled sends. Seven student organizations and the City of Medina use it.',
    facts:[['Built with','Web app · SMS and email'],['My role','Co-founder & founding engineer'],['Status','In use since 2025'],['Users','7 student orgs · City of Medina']],
    look:{fur:'#c98b4f', hat:'#0c1f18', vest:'#0f3d2e', shirt:'#f5f0e6', pants:'#0f3d2e'} },
  { id:'vid', name:'VidUnderstand', rank:'8', suit:'♣', short:'Search hours of video for the moment you need.',
    line:'I watch your videos so you don’t have to. Upload hours of footage, jump straight to the moment you need, and I’ll write the document from what happened. Want a look?',
    more:'A Rust backend does the heavy lifting, Gemini does the watching, and a Next.js front end ties it together. Search is by meaning, not file names.',
    facts:[['Built with','Rust, Next.js, Gemini'],['Built','Oct–Nov 2025'],['Demo','https://youtu.be/LovM-rcPZ-I?t=55'],['Code','https://github.com/EyalShechtman/open-ai-video-understanding']],
    look:{fur:'#e0bd86', hat:'#201a26', vest:'#3d2b4e', shirt:'#f6f2ea', pants:'#3d2b4e'} }
];
export const DEALER_LOOK = {fur:'#a87443', hat:'#121212', vest:'#101012', shirt:'#fbfaf6', pants:'#101012'};
export const DOG_LOOK = {fur:'#ddb683', hat:'#6b4226', vest:'#4c5631', shirt:'#e7d8b8', pants:'#4a5230'};
export const CHAPTERS = {
  projects:{ rank:'A', suit:'♦', kick:'Behind the flag', title:'The projects', body:'Every player at the table is a chapter of my work. Sit in the empty chair and they’ll deal you in one by one, or read the whole hand here.', grid:PLAYERS.map(p => [p.name, p.short]).concat([['Also built', 'mdxx · AWS Hack Day · RoamRich (DubHacks) · Sammamish Pickleball app · VideoArchive · AutomatedAds · ArtistOS · Casca'], ['All the code', 'https://github.com/EyalShechtman']]) },
  soccer:{ rank:'10', suit:'♣', kick:'Chapter · The pitch', title:'The soccer years', body:'Most of my weekends growing up were spent on a pitch: club soccer with Bellevue Athletic FC in the ECNL, and my high school team. The album on the wall has the photos. The TV has the highlights.', grid:[['Club','Bellevue Athletic FC'],['League','ECNL'],['Number','12'],['Highlights','https://www.youtube.com/@eyalshechtman7050']] },
  contact:{ rank:'J', suit:'♥', kick:'All in', title:'Let’s talk', body:'You pushed your chips in. Here’s where to find me.', grid:[['Email','mailto:eyal.shechtman@gmail.com'],['LinkedIn','https://www.linkedin.com/in/eyal-shechtman'],['X','https://x.com/EyalShechtman'],['GitHub','https://github.com/EyalShechtman'],['YouTube','https://www.youtube.com/@eyalshechtman7050'],['Chess.com','https://www.chess.com/member/EyalShechtman12']] }
};
