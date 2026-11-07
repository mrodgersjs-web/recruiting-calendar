const fs=require('fs');
// condensed block glyphs on 44x100 grid, stroke 15
const S=15,W=44,H=100;
const R=(x,y,w,h)=>`M${x} ${y}h${w}v${h}h${-w}z`;
const G={
T:[R(0,0,W,S),R((W-S)/2,0,S,H)],
H:[R(0,0,S,H),R(W-S,0,S,H),R(0,42,W,S)],
E:[R(0,0,S,H),R(0,0,W,S),R(0,43,W-6,S-1),R(0,H-S,W,S)],
C:[`M0 12a12 12 0 0 1 12-12h${W-12}v${S}h${-(W-S-6)}a6 6 0 0 0-6 6v${H-2*S-12}a6 6 0 0 0 6 6h${W-S-6}v${S}h${-(W-12)}a12 12 0 0 1-12-12z`],
O:[`M12 0h${W-24}a12 12 0 0 1 12 12v${H-24}a12 12 0 0 1-12 12h${-(W-24)}a12 12 0 0 1-12-12v${-(H-24)}a12 12 0 0 1 12-12z M${S+5} ${S}a5 5 0 0 0-5 5v${H-2*S-10}a5 5 0 0 0 5 5h${W-2*S-10}a5 5 0 0 0 5-5v${-(H-2*S-10)}a5 5 0 0 0-5-5z`],
M:[R(0,0,S,H),R(54-S,0,S,H),`M0 0h${S}l12 40l12-40h${S}l-20 64h-8z`],
I:[R(0,0,S,H)],
B:[`M0 0h${W-10}a10 10 0 0 1 10 10v28a8 8 0 0 1-5 7a8 8 0 0 1 5 7v38a10 10 0 0 1-10 10h${-(W-10)}z M${S} ${S}v${43-S}h${W-2*S}v${-(43-S)}z M${S} 57v${H-S-57}h${W-2*S}v${-(H-S-57)}z`],
K:[R(0,0,S,H),`M${S} 40l${W-S-14} -40h16l-26 50l26 50h-16l${-(W-S-14)} -40z`],
};
const wid={M:54,I:S};
function word(str,x0,y0,sc,gap=7,sp=26){let x=x0,p=[];for(const ch of str){if(ch==' '){x+=sp*sc;continue}const w=wid[ch]||W;p.push(`<g transform="translate(${x} ${y0}) scale(${sc})" fill-rule="${"OB".includes(ch)?"evenodd":"nonzero"}"><path d="${G[ch].join(' ')}"/></g>`);x+=(w+gap)*sc}return{svg:p.join(''),w:x-x0-gap*sc}}
// MARK: square badge, open book spine forms a chevron "commit" arrow; tab notch top-right
function mark(fg,bg){return `<rect width="64" height="64" rx="6" fill="${fg}"/><path fill="${bg}" d="M14 18h14l4 4 4-4h14v26H36l-4 4-4-4H14z M19 23v16h10l3 3 3-3h10V23h-8l-5 5-5-5z"/><path fill="${bg}" d="M28 31l3 3 6-7 2.5 2.2L31 38.5l-5.5-5.3z"/>`}
const out=(n,w,h,body,bg)=>fs.writeFileSync(n,`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">${bg?`<rect width="100%" height="100%" fill="${bg}"/>`:''}${body}</svg>\n`);
for(const [t,fg,bg] of [['light','#000','#fff'],['dark','#fff','#000']]){
 out(`mark-${t}.svg`,64,64,mark(fg,bg));
 const a=word('THE',0,0,.4),b=word('COMMIT BOOK',0,52,1);
 out(`wordmark-${t}.svg`,Math.ceil(b.w),152,`<g fill="${fg}">${a.svg}</g><g fill="${fg}">${b.svg}</g>`,bg);
 const c=word('COMMIT BOOK',150,40,.8),d=word('THE',150,0,.3);
 out(`lockup-horizontal-${t}.svg`,Math.ceil(150+c.w+20),130,`<g transform="translate(0 0) scale(2.03)">${mark(fg,bg)}</g><g fill="${fg}">${d.svg}${c.svg}</g>`,bg);
 const e=word('COMMIT BOOK',0,0,.6);const ox=(Math.max(e.w,200)-e.w)/2, W2=Math.ceil(Math.max(e.w,200));
 out(`lockup-stacked-${t}.svg`,W2,280,`<g transform="translate(${(W2-192)/2} 0) scale(3)">${mark(fg,bg)}</g><g fill="${fg}"><g transform="translate(${ox} 220)">${e.svg}</g></g>`,bg);
 const f=word('COMMIT BOOK',80,300,1.25),g=word('THE',80,240,.45);
 out(`social-card-${t}.svg`,1200,630,`<g transform="translate(80 80) scale(2)">${mark(fg,bg)}</g><g fill="${fg}">${g.svg}${f.svg}</g><text x="80" y="540" fill="${fg}" font-family="Helvetica Neue, Arial, sans-serif" font-weight="700" font-size="34" letter-spacing="2">REAL ATHLETE STORIES. THE PLAYBOOKS BEHIND THEM.</text><rect x="80" y="470" width="120" height="8" fill="${fg}"/>`,bg);
}
// favicon: simplified, thicker
fs.writeFileSync('favicon.svg',`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect width="16" height="16" rx="2" fill="#000"/><path fill="#fff" d="M3 4h4l1 1 1-1h4v8H9l-1 1-1-1H3z"/><path d="M6 8l1.5 1.5L10.5 6" stroke="#000" stroke-width="1.6" fill="none"/></svg>\n`);
