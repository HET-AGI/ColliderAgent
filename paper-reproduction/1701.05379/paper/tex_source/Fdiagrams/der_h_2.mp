% Fdiagrams/der_h_2.mp -- do not edit, generated automatically by Draft_05_19.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 40*1.0pt#, 30*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vtop (__tl, __tc, __tr);
vleft (__bl, __in, __tl);
vright (__br, __out, __tr);
vconnect ("photon", __tl, __v);
vconnect ("dashes", __bl, __v);
vconnect ("dashes", __v, __tr);
vconnect ("dashes", __v, __br);
vlabel ("$Z_\m $", __tl);
vlabel ("$a$", __bl);
vlabel ("$h$", __tr);
vlabel ("$h$", __br);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
