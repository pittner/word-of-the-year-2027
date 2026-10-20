#!/usr/bin/env python3
"""Builds index.html for pittner/word-of-the-year-2027.

A single-purpose page for the seasonal "word of the year 2027" / "one word 2027" intent
(people pick a word for the new year in December-January): 48 words in 6 groups, each with
a one-line meaning and a first step, and a link that opens the free phone maker with that
word and first step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098).
Plus a box for your own word, how to choose a word, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/word-of-the-year-2027/"
SRC = "ghpages_word"
CAMPAIGN = "word_2027"

# (group, [(word, what it means in a year, a first step small enough for this week)])
GROUPS = [
    ("Calm and rest", [
        ("Calm", "Fewer things decide my mood for me.", "Ten quiet minutes before I open my phone"),
        ("Slow", "I stop rushing the things that matter.", "Eat one meal this week without a screen"),
        ("Rest", "Rest is part of the plan, not the reward.", "Put a bedtime alarm on my phone tonight"),
        ("Peace", "I choose which fights are worth it.", "Mute one group chat that drains me"),
        ("Simplify", "Less stuff, fewer commitments, more room.", "Clear one drawer on Saturday"),
        ("Breathe", "A pause before I react.", "Three slow breaths before I answer a hard message"),
        ("Enough", "I stop chasing more than I need.", "Write down three things I already have and like"),
        ("Gentle", "I talk to myself like I talk to a friend.", "Replace one harsh thought with a kind sentence today"),
    ]),
    ("Growth and courage", [
        ("Brave", "I do the thing while I am still scared.", "Send the message I have been putting off"),
        ("Begin", "Starting matters more than starting perfectly.", "Spend 15 minutes on the first draft today"),
        ("Grow", "I am allowed to be a beginner again.", "Sign up for one class or course this month"),
        ("Bold", "I ask for what I want.", "Ask for one thing I would normally not ask for"),
        ("Become", "I act like the person I want to be.", "Write one sentence about who I am becoming"),
        ("Try", "More experiments, fewer verdicts.", "Try one new thing this week and note what happened"),
        ("Rise", "Setbacks are part of the climb.", "Name one setback from 2026 and what it taught me"),
        ("Open", "I say yes to more than I usually would.", "Say yes to one invitation this month"),
    ]),
    ("Focus and discipline", [
        ("Focus", "One thing at a time, done well.", "Pick my one priority for tomorrow tonight"),
        ("Finish", "I complete what I start.", "List my unfinished projects and pick one to finish"),
        ("Commit", "Fewer promises, kept every time.", "Put my most important goal in the calendar"),
        ("Consistent", "Small things, every day.", "Do the habit for 5 minutes, even on bad days"),
        ("Discipline", "I do it when I do not feel like it.", "Lay out tomorrow's clothes for the workout tonight"),
        ("Clarity", "I know what I want and say it.", "Write my three goals for 2027 on one page"),
        ("Intention", "I decide before the day decides for me.", "Write the first line of tomorrow's plan tonight"),
        ("Done", "Done is better than perfect.", "Ship one thing this week at 80 percent"),
    ]),
    ("Health and energy", [
        ("Strong", "A body that carries me well.", "Two short strength sessions this week"),
        ("Move", "I move every day, a little.", "A 20-minute walk after lunch today"),
        ("Nourish", "Food that makes me feel good later.", "Plan three dinners for this week"),
        ("Energy", "I protect what gives me energy.", "Write down what drained me today and what charged me"),
        ("Heal", "I take care of what hurts.", "Book the appointment I keep postponing"),
        ("Vitality", "More good days than tired days.", "Drink a glass of water before my morning coffee"),
        ("Sleep", "Sleep comes first, the rest follows.", "Phone out of the bedroom tonight"),
        ("Balance", "Work, rest and people all get a turn.", "Block one evening this week with no work at all"),
    ]),
    ("Money and work", [
        ("Abundance", "I notice what is working.", "Write three wins from this week"),
        ("Build", "I build something that lasts.", "Spend one hour on my own project this weekend"),
        ("Save", "Future me gets paid first.", "Set up an automatic transfer on payday"),
        ("Create", "I make more than I consume.", "Make one small thing this week and show someone"),
        ("Lead", "I take responsibility and go first.", "Volunteer for one thing at work this month"),
        ("Freedom", "More choices about my own time.", "Write down what freedom would look like on a Tuesday"),
        ("Worth", "I charge and ask for what I am worth.", "Look up the market rate for my work"),
        ("Launch", "I put my work out into the world.", "Pick a launch date and tell one person"),
    ]),
    ("People and joy", [
        ("Joy", "I make room for what makes me light.", "Do one thing just because it is fun this weekend"),
        ("Connect", "Fewer screens, more real conversations.", "Call one friend this week instead of texting"),
        ("Love", "I show it, not only feel it.", "Tell someone what I appreciate about them today"),
        ("Present", "I am where my feet are.", "Leave my phone in another room during dinner"),
        ("Play", "Not everything needs to be productive.", "Plan one afternoon with no goal at all"),
        ("Gratitude", "I notice the good on ordinary days.", "Write one thing I am thankful for before bed"),
        ("Adventure", "I go somewhere new.", "Pick one place to visit in 2027 and put it in the calendar"),
        ("Home", "A place that feels good to come back to.", "Fix one small thing at home this week"),
    ]),
]

HOW = [
    ("Look back at 2026.", "Write the three moments you are proud of and the three you would do differently. Your word usually sits between the two lists."),
    ("Ask one question.", "\"What do I want to feel more of in 2027?\" Answer with one word, not a goal. Calm, brave, strong, free."),
    ("Test it with a decision.", "Imagine a normal busy Tuesday. Does the word tell you what to say yes or no to? If it does, keep it."),
    ("Put it where you will see it.", "A word you see 80 times a day on your lock screen works better than one written once in a notebook."),
]

FAQ = [
    ("What is a word of the year?",
     "One word you choose to guide the coming year instead of, or next to, a list of resolutions. It names how you want to live or feel, "
     "for example calm, brave or focus, and you use it to decide what to say yes or no to."),
    ("How do I choose my word for 2027?",
     "Look back at 2026, ask what you want to feel more of in 2027, and test the word with an ordinary decision. If it tells you what to do on a busy day, it is your word. "
     "There are 48 ideas with a meaning and a first step on this page."),
    ("What are good words of the year?",
     "Words that point to a feeling or a way of acting: calm, brave, focus, strong, joy, finish, simplify, connect. "
     "A good word is short, positive and easy to remember when you are tired."),
    ("How do I remember my word all year?",
     "Make it visible. The free maker on this page turns your word and a first step into a 1080x1920 lock-screen image, so you see it every time you pick up your phone."),
    ("Is the lock-screen maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. You type or pick a word, add a first step and save the image."),
    ("Can I make a full vision board around my word?",
     "Yes. Start from your word in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]


def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(word, step, content):
    return link("/free-vision-board-maker/", goal=word, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="hero_tool")
AI = link("/en/create.php", utm_content="faq_ai")
WALL_2027 = link("/2027-vision-board-wallpaper/", utm_content="more_wall2027")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def build():
    count = sum(len(ws) for _, ws in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, words in GROUPS:
        cards = []
        for w, meaning, step in words:
            cards.append(
                f'      <div class="wcard" id="w-{slug(w)}"><h3>{e(w)}</h3><p>{e(meaning)}</p>'
                f'<p class="step"><span>First step:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(w, step, "word_" + slug(w)))}" data-cta="word_{slug(w)}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    how = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in HOW)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%HOW%%": how, "%%FAQ%%": faq_html, "%%LD%%": ld,
        "%%COUNT%%": str(count), "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%WALL%%": e(WALL_2027), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "words")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Word of the Year 2027: %%COUNT%% Ideas, How to Choose Yours &amp; a Free Lock Screen</title>
<meta name="description" content="%%COUNT%% word of the year ideas for 2027, each with what it means and a first step for this week. Pick one or type your own and turn it into a free phone lock screen. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Word of the year 2027 - %%COUNT%% ideas and a free lock screen">
<meta property="og:description" content="Pick your one word for 2027, see what it means and a first step, and save it as your phone lock screen. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#6D28D9;--bg:#FBFAF9}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#5B21B6;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
@media (max-width:960px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 22px/1.2 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how{max-width:70ch;color:#374151;padding-left:22px}
ol.how li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Word of the year 2027: %%COUNT%% ideas and a lock screen to keep it</h1>
  <p class="lede">Instead of ten resolutions, pick one word for 2027 that tells you what to say yes or no to. Below are %%COUNT%% words, each with what it means in a year and a first step for this week. Press a word and it opens on a free phone lock screen with the first step under it, ready to save. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% words in 6 groups &middot; 1080&times;1920 lock screen &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already have your word?</h2>
  <div class="row">
    <div><label for="ownWord">My word for 2027</label><input id="ownWord" maxlength="40" placeholder="e.g. Brave" autocomplete="off"></div>
    <div><label for="ownStep">My first step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Send the message I have been putting off" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your word filled in. You can change colors and layout there before you save.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%%</nav>

%%GROUPS%%

<section class="block">
  <h2>How to choose your word in 10 minutes</h2>
  <ol class="how">
%%HOW%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="how_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%WALL%%" data-cta="more_wall2027">20 ready 2027 goals as wallpapers</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board around my word</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/word-of-the-year-2027">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own word: same prefill as the word cards (?goal=&step=&layout=text&mode=wallpaper).
  var w=document.getElementById('ownWord'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var word=w.value.trim(),step=s.value.trim();
    if(!word){ msg.textContent='Type your word first.'; w.focus(); return; }
    var q=new URLSearchParams({goal:word,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_word',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_word');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [w,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
