from queue import PriorityQueue
from typing import TYPE_CHECKING, Sequence, Mapping, Tuple, Union
from core.entities import *
from core.rules import *
from core.simulation.operation import *
from core.simulation.constraint import *


class Simulation:
    def __init__(self):
        self.characters: Mapping[str, Character_] = {}
        self.artifactmap: Mapping[str, Artifact] = {}
        # self.weaponmap: Mapping[str, Weapon] = {}
        self.operation_track: Sequence[Operation] = []
        self.constraint_track: Sequence[Constraint] = []
        self.recorder = []

    def set_character(self, name='', lv=1, asc=False):
        if name not in self.characters.keys() and len(self.characters) <= 4:
            tmp = Character_()
            tmp.base.choose(name)
            tmp.base.set_lv(lv, asc)
            self.characters[name] = tmp
            self.artifactmap[name] = Artifact()
            # self.weaponmap[name] = Weapon()
        elif name in self.characters:
            self.characters[name].base.set_lv(lv, asc)
        else:
            raise Exception('error occur when setting the character')

    def del_characters(self, name=''):
        if name not in self.characters.keys():
            raise KeyError
        else:
            del self.characters[name]
            del self.artifactmap[name]
            # del self.weaponmap[name]

    def set_artifact(self, name='', art={}):
        self.artifactmap[name].artifacts[0].initialize(art)
        return
    
    def insert(self, obj: Union['Operation', 'Constraint']):
        if isinstance(obj, Operation):
            self.operation_track.append(obj)
        elif isinstance(obj, Constraint):
            self.constraint_track.append(obj)
        else:
            raise TypeError
    
    def remove(self, obj: Union['Operation', 'Constraint']):
        try:
            if isinstance(obj, Operation):
                self.operation_track.remove(obj)
            elif isinstance(obj, Constraint):
                self.constraint_track.remove(obj)
        except ValueError:
            raise ValueError('obj not found')
        except TypeError:
            raise TypeError('please input operation or constraint')
        else:
            return

    def start(self):
        '''
        每一次模拟配置生成一个实例
        同样的配置项可以多次执行计算(考虑到例如暴击率的效果每次执行的结果是随机的，暴击率也可以设置成折算为期望收益)
        '''
        print('CALCULATE START!')
        operation_queue: PriorityQueue[Tuple[float, Operation]] = PriorityQueue()
        active_constraint: Sequence[Constraint] = []
        active_constraint.extend(self.constraint_track)
        list(map(lambda op: operation_queue.put(
            (op.priority, op)), self.operation_track))
        while operation_queue.unfinished_tasks > 0:
            op: Operation = operation_queue.get()[1]
            op.execute(self)
            self.recorder.append(op.desc)
            operation_queue.task_done()
        print('CALCULATE FINISHED!')
