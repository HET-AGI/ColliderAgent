% Fdiagrams/Zhhcoupl.mp -- do not edit, generated automatically by "Feynman Rules alp_higgs".tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 50*1.0pt#, 50*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__i1);
vright (__o2, __o1);
vconnect ("boson", __i1, __v1);
vconnect ("dashes", __v1, __o1);
vconnect ("dashes", __v1, __o2);
vvertex ("lab=$h$,l.angle=0", __o1);
vvertex ("lab=$h$,l.angle=0", __o2);
vvertex ("lab=$Z_\mu $,l.angle=180", __i1);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
