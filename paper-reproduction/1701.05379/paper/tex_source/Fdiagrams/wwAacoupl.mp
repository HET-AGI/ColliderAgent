% Fdiagrams/wwAacoupl.mp -- do not edit, generated automatically by EPJC_V2.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 90*1.0pt#, 50*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1, __i2);
vright (__o2, __o1);
vconnect ("dashes", __i2, __v1);
vconnect ("boson", __i1, __v1);
vconnect ("boson", __v1, __o1);
vconnect ("boson", __v1, __o2);
vvertex ("lab=$W^+_\mu $,l.angle=0", __o1);
vvertex ("lab=$W^-_\nu $,l.angle=0", __o2);
vvertex ("lab=$A_\rho $,l.angle=180", __i1);
vvertex ("lab=$a$,l.angle=180", __i2);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
