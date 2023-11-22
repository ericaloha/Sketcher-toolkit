#! /bin/bash
#echo "Ftrace Start!" > /home/hkc-nfs/Ftrace.log
echo 1 > /tracing/tracing_on
#echo function_graph > /tracing/current_tracer
echo 1 > /tracing/events/nfs4/enable
echo 0 > /tracing/events/nfs4/nfs4_cb_sequence/enable
echo 0 > /tracing/events/nfs4/nfs4_sequence_done/enable
echo 0 > /tracing/events/nfs4/nfs4_cb_sequence/enable
echo 0 > /tracing/events/nfs4/nfs4_setup_sequence/enable
echo 0 > /tracing/events/nfs4/nfs4_open_stateid_update/enable
echo 0 > /tracing/events/nfs4/nfs4_cached_open/enable
#echo '*nfs4*' > set_ftrace_filter
#echo '*sequence*' > set_ftrace_notrace
echo "START of TEST: hkc" > /tracing/trace_marker
