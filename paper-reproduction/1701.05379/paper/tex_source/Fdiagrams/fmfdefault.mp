% fmfdefault.mp -- do not edit, generated automatically by FR_axion.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 50*1.0pt#, 10*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vleft (__bl, __in);
vright (__br, __out);
vconnect ("photon", __in, __v);
vconnect ("dashes", __v, __out);
vvertex ("decor.shape=cross", __v);
vlabel ("$Z_\mu $", __in);
vlabel ("$a$", __out);
vlabel ("$\sim \frac {-2ig}{f_a} {c}_9 p_z^2 p_a$", __v);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
