from plantuml import PlantUML

# 配置 PlantUML 服务器 (本地或远程)
# 如果在本地配置了 PlantUML 环境，可以直接使用
plantuml = PlantUML(url='http://localhost:8080/plantuml')

# ================= 场景一：基础逻辑（5.1/5.2/5.3 的循环与分支） =================
# 描述：机械臂循环检测，根据条件进入不同状态
sequence_code_1 = """
@startuml
skinparam sequenceArrowThickness 2
skinparam participantPadding 20

title 场景一：机械臂检测空位与状态分支

participant "机械臂" as Robo
participant "南师大叫号" as Call
database "缓冲区" as Buffer

== 初始化 ==
Robo -> Robo: 5. 检测是否有缓冲区空位

== 循环检测逻辑 ==
loop 直到满足发药条件
    alt 有空位 且 有排队患者
        Robo -> Robo: 5.1 判定为可发药
        Robo -> Call: 5.1.1 叫号上屏
        Robo -> Robo: 结束当前循环，处理叫号
    else 有空位 且 无排队患者
        Robo -> Robo: 5.2 判定为等待患者
        Robo -> Call: 5.2.1 叫号上屏 (提示等待)
        note right: 5.2 需要等待至有患者\n然后变成 5.1
        Robo -> Robo: 继续循环检测
    else 无空位 且 有排队患者
        Robo -> Robo: 5.3 判定为等待空位
        Robo -> Call: 5.3.1 叫号上屏 (提示拥挤)
        note right: 5.3 需要等待至有空位\n然后变成 5.1
        Robo -> Robo: 继续循环检测
    end
end

@enduml
"""

# 生成图表
print("正在生成场景一图表...")
img1 = plantuml.processes(sequence_code_1)
with open("scenario_1.png", "wb") as f:
    f.write(img1)
print("场景一图表已保存为 scenario_1.png")

# ================= 场景二：并发动作处理 =================
# 描述：机械臂在“等待空位”时，同时触发“内部检测”和“叫号系统更新”
sequence_code_2 = """
@startuml
skinparam sequenceArrowThickness 2

title 场景二：并发动作处理（内部检测与叫号并行）

participant "患者" as Patient
participant "机械臂" as Robo
participant "HIS" as His
participant "Rowa" as Rowa
participant "南师大叫号" as Call

== 并发场景：5.3 等待空位期间 ==
Robo -> Robo: 5.3 检测到无空位\n但有待发药患者

par 并发处理开始
    Robo -> Robo: 启动内部检测线程
    Robo -> His: 查询库存状态 (非阻塞)
    Robo -> Rowa: 预占资源检查 (非阻塞)
    
    Robo -> Call: 5.3.1 叫号上屏\n(提示：请稍候，缓冲区满)
    
    Robo -> Robo: 等待任一事件发生：\n1. 缓冲区空位出现\n2. 患者取药完成
end

== 事件触发后 ==
Robo -> Robo: 监听到缓冲区空位释放
Robo -> Robo: 退出等待状态
Robo -> Robo: 转入 5.1 状态
Robo -> Call: 5.1.1 正式叫号上屏

@enduml
"""

# 生成图表
print("正在生成场景二图表...")
img2 = plantuml.processes(sequence_code_2)
with open("scenario_2.png", "wb") as f:
    f.write(img2)
print("场景二图表已保存为 scenario_2.png")