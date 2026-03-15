% Fdiagrams/addcoupl.mp -- do not edit, generated automatically by EPJC_V2.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 50*1.0pt#, 50*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1, __i2, __i3);
vright (__o3, __o2, __o1);
vconnect ("dashes", __i2, __v1);
vconnect ("fermion,label=$D_\beta $", __o1, __v1);
vconnect ("fermion,label=$D_\alpha $", __v1, __o3);
vvertex ("lab=$a$", __i2);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
