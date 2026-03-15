% Fdiagrams/VBFgdiag.mp -- do not edit, generated automatically by Draft_20jan.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 80*1.0pt#, 40*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1, __i2, __i3);
vright (__o1, __o2, __o4, __o3);
vconnect ("fermion,tension=2", __i1, __v1, __o1);
vconnect ("fermion,tension=2", __i3, __v3, __o3);
vconnect ("boson,lab=$W$,tension=2", __v1, __v2, __v3);
vconnect ("dashes", __v2, __o2);
vconnect ("boson", __v2, __o4);
vvertex ("lab=$a$", __o2);
vvertex ("lab=$q$", __i1);
vvertex ("lab=$q^\prime $", __i3);
vvertex ("lab=$\gamma $", __o4);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
