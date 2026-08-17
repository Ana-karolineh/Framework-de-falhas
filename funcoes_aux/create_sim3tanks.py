import itertools
import os
import platform
import sys
_global_counter = itertools.count(1)

def create_sim3tanks():
    from src.sim3tanks.sim3tanks import Sim3Tanks, Struct
    tts = Sim3Tanks()
    tts.About = Struct(Name='Sim3Tanks', Version='2.0.2', Description='A Benchmark Model Simulator for Process Control and Monitoring', License='MIT', Link='https://github.com/e-controls/Sim3Tanks', CurrentPath=os.getcwd(), PythonVer=sys.version, SystemArch=platform.machine(), ObjectID=next(_global_counter))
    return tts
