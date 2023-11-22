#! /bin/bash
#echo "Ftrace Stop!" > /home/hkc-nfs/Ftrace.log
echo "END of TEST: hkc " > /tracing/trace_marker
echo 0 > /tracing/events/nfs4/enable
echo 0 > /tracing/tracing_on
