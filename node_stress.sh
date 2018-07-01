#!usr/bin/sh

stress_time=30

# 0.5x
/usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 $stress_time  --initial-reg-rate 100 \
            --multiplier 225 
# 1.0x
/usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 $stress_time  --initial-reg-rate 100 \
            --multiplier 450 
# 1.5x
/usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 $stress_time  --initial-reg-rate 100 \
            --multiplier 675 
# 2.0x
/usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 $stress_time  --initial-reg-rate 100 \
            --multiplier 900 
# 2.5x
/usr/share/clearwater/bin/run_stress default.svc.cluster.local \
            500 $stress_time  --initial-reg-rate 100 \
            --multiplier 1125 


# P:Peridoc
# FailedCall(P)/OutgoingCall(P) = FailRate