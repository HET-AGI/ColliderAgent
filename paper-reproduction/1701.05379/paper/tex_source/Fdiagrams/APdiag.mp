% Fdiagrams/APdiag.mp -- do not edit, generated automatically by Draft_20jan.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 80*1.0pt#, 30*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1, __i2, __i3);
vright (__o3, __o2, __o1);
vconnect ("fermion", __i1, __v1);
vconnect ("fermion", __v1, __i3);
vconnect ("boson,lab=$W$", __v1, __v2);
vconnect ("boson", __v2, __o3);
vconnect ("dashes", __v2, __o1);
vvertex ("lab=$W$,l.angle=0", __o3);
vvertex ("lab=$a$", __o1);
vvertex ("lab=$q$", __i1);
vvertex ("lab=$q^\prime $", __i3);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
