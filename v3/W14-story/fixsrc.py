import pathlib,re,sys
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
p=pathlib.Path("site/assets/deck.js"); t=p.read_text(encoding="utf-8")
old="""var SRC_LINK = function (a) {
  if (!a) return '/how-we-source';
  if (a.page === false) return '/playbooks#sources';
  return (a.source && /^https?:/.test(a.source)) ? a.source : ('/story/' + a.id + '#sources');
};"""
new="""var SRC_LINK = function (a) {
  if (!a) return '/how-we-source';
  if (a.page === false) {
    /* a composite has no bio page; send the question to the playbook's own sources block */
    var pb = (a.related || [])[0];
    return pb ? '/playbooks/' + pb + '#sources' : '/how-we-source';
  }
  return (a.source && /^https?:/.test(a.source)) ? a.source : ('/story/' + a.id + '#sources');
};"""
print("pattern present:", old in t)
p.write_text(t.replace(old,new),encoding="utf-8")
