from PIL import Image
import hashlib, pathlib, collections
M = pathlib.Path(r"C:\Users\Jloeh\Developer\recruiting-calendar\site\assets\media")
def h(p): return hashlib.md5(p.read_bytes()).hexdigest()[:10]
for f in ["cut-derrick-640.webp","cut-derrick-1080.webp","cut-wbasketball-640.webp","cut-football-640.webp","cut-volleyball-640.webp"]:
    p = M / f
    print("%-28s md5=%s" % (f, h(p)), end="  ")
    im = Image.open(p).convert("RGBA")
    a = im.getchannel("A")
    cov = sum(1 for v in a.getdata() if v > 8) / (im.size[0]*im.size[1])
    px = list(im.getdata())
    solid = [(r,g,b) for (r,g,b,al) in px if al > 200]
    def near(c, t, d=45): return all(abs(x-y) <= d for x, y in zip(c, t))
    navy = sum(1 for c in solid if near(c, (20, 30, 70), 40) and c[2] > c[0])
    gold = sum(1 for c in solid if near(c, (210, 165, 45), 45))
    white = sum(1 for c in solid if min(c) > 210)
    orange = sum(1 for c in solid if c[0] > 150 and 40 < c[1] < 130 and c[2] < 80)
    chroma = sum(1 for c in solid if c[1] > 170 and c[0] < 110 and c[2] < 110)
    sat = [max(c)-min(c) for c in solid] or [(0,)]
    print("size=%s aspect=%.4f covered=%.1f%% mean_sat_on_figure=%.1f" % (im.size, im.size[0]/im.size[1], 100*cov, sum(sat)/len(sat)),
          "| navy %.1f%% gold %.1f%% white %.1f%% ball-orange %.1f%% leftover-chroma %.2f%%" % tuple(
              100*n/len(solid) for n in (navy, gold, white, orange, chroma)))
