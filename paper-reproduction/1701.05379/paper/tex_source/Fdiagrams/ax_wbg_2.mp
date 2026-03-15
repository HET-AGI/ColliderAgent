% Fdiagrams/ax_wbg_2.mp -- do not edit, generated automatically by FileGordo_GBs@Collider.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 60*1.0pt#, 35*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__bl, __in);
vright (__br, __out);
vconnect ("photon", __in, __v);
vconnect ("dashes", __v, __out);
vvertex ("decor.shape=cross,d.size=8", __v);
vlabel ("$Z_\mu $", __in);
vlabel ("$a$", __out);
vlabel ("$\frac {-2ig}{f_a} {c}_9 p_z p^2_a$", __v);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
