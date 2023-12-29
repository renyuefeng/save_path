import pandas as pd
import re
import numpy as np
from snownlp import SnowNLP
import jieba

# 机油标签
def modelClean(data_cc, col='', out_model='model1'):
    pattern = re.compile(
        '美孚一号金装 经典表现|美孚新速霸2000-抗磨倍护|美孚新速霸1000-每日保护|美孚新速霸-全效保护|美孚速霸高性能|美孚1号静逸|美孚1号-风尚版|美孚1号黑美|美孚速霸-畅途版|'
        '美孚速霸-安途版|美孚1号长里程|美孚1号燃油经济|美孚1号涡轮增压|美孚1号混合动力|美孚1号-黑金版|美孚1号雷霆4T|美孚1号金美|美孚速霸2000|美孚速霸1000|美孚MT80|美孚旋风4T|美孚超级4T|美孚万能4T|'
        '美孚雷霆4T|美孚小霸王2T|美孚润滑脂XHP222|美孚路宝GX|美孚润滑脂MP|美孚力霸特级|美孚力霸9000|美孚自动变速箱油 |美孚刹车油 |美孚速霸全效保护|美孚1号长效机滤|美孚1号动逸|美孚1号全合成机油|'
        '美孚滑脂MP|嘉实多引擎洁霸|美孚1号机油滤清器长效款|美孚力霸|壳牌鹏致P7 Pro|壳牌鹏致P8 Pro|壳牌鹏致P9 Pro|壳牌喜力HX7 PLUS|壳牌喜力HX5 Plus|壳牌喜力HX5 PLUS|壳牌超凡喜力中超版|'
        '壳牌极净超凡喜力-零碳环保|壳牌超凡喜力-零碳环保|壳牌超凡喜力千里江山版|壳牌超凡喜力都市光影|壳牌超凡喜力-高效动力|壳牌喜力HX7|壳牌喜力HX5|壳牌喜力HX6|壳牌喜力HX3|壳牌喜力HX8|壳牌超凡喜力-焕耀版|'
        '壳牌锐净超凡喜力-零碳环保|锐净零碳全合成油|壳牌先锋超凡喜力千里江山版|壳牌恒护超凡喜力|壳牌极净超凡喜力千里江山版|壳牌喜力混动先锋|壳牌爱德王子ULTRA PLUS|壳牌动力巅峰|壳牌鹏致CP8|壳牌鹏致EP9|壳牌施倍力S6|'
        '壳牌施倍力S5|壳牌施倍力S4|壳牌施倍力S3|壳牌施倍力S2|壳牌鹏致N7|壳牌鹏致SP7|壳牌爱德王子AX5|壳牌爱德王子AX7|壳牌爱德王子AX3|壳牌劲霸|壳牌恒护超凡喜力-零碳环保|壳牌劲霸柴机油|壳牌劲霸R3|壳牌劲霸R2|'
        '壳牌劲霸LD4|壳牌清洁油|壳牌劲霸LD3|嘉实多超级奔程|嘉实多极护supercar|嘉实多磁护混合动力|嘉实多大力士CK-4|嘉实多大力士CI-4|嘉实多磁护SUV|嘉实多磁护启停保|嘉实多磁护专享|嘉实多极护专享|嘉实多金嘉护|'
        '嘉实多超嘉护|嘉实多银嘉护|嘉实多嘉力|嘉实多极护|嘉实多磁护|嘉实多大力士|美孚黑霸王CH-4|美孚黑霸王CI-4|美孚黑霸王CF-4|美孚黑霸王长效(X系列)|美孚黑霸王长效CK-4|美孚黑霸王长效CJ-4|美孚黑霸王傲超|'
        '美孚黑霸王傲超(K系列)|美孚黑霸王1号|美孚黑霸王高效|美孚黑霸王超高级|美孚黑霸王超级|美孚黑霸王特级|美孚黑霸王合成级|美孚黑霸王城市之星|美孚黑霸王单级|美孚黑霸王燃气发动机油|美孚黑霸王畅行系列|'
        '美孚黑霸王工程机械发动机油|美孚黑霸王工程机械液压油|美孚黑霸王齿轮油|美孚润滑脂XHP223|美孚路宝车用齿轮油GX|美孚黑霸王防冻液|美孚传动油(美孚424)|美孚力图H|美孚自动变速箱油|美孚刹车油|壳牌劲霸K15|'
        '壳牌劲霸K10|壳牌劲霸K8|壳牌劲霸K6|壳牌劲霸K4|壳牌劲霸R6 LM|壳牌重载HD6|壳牌车队专享特级柴油机润滑油|壳牌车队专享高级柴油机润滑油|壳牌车队专享超级柴油机润滑油|嘉实多超劲活能|嘉实多超霸|嘉实多超级奔腾|'
        '潍柴专用机油|潍柴专用机油锐动力|长城尊龙T600|长城尊龙T700|昆仑天威|一汽解放发动机润滑油|道达尔红运 7900|道达尔红运优选 1100|统一钛粒王|统一油压王|康明斯|东风长里程|东风超级柴油机油|道达尔快驰 INEO|'
        '道达尔快驰4000|道达尔快驰5000|道达尔快驰7000|道达尔快驰8000|道达尔快驰9000|道达尔经典系列CLASSIC 9|昆仑润盛|昆仑GL|昆仑车掌柜|昆仑润福|昆仑天润|昆仑润强|昆仑润威|龙蟠SONIC T1|'
        '龙蟠SONIC9000|龙蟠1号|龙蟠SONIC7000|龙蟠净威|龙蟠智尊|龙蟠SONIC F1|龙蟠SONIC N1|龙蟠Trisonic|龙蟠SONIC T3|统一润滑油擎锋4000|统一润滑油经典A3|统一润滑油OEM|统一润滑油擎锋3000|'
        '统一润滑油擎锋M5000|统一润滑油京保养|统一润滑油擎锋M3000|统一润滑油经典A0|统一润滑油经典A1|统一润滑油莫托维克|统一润滑油神行者|统一润滑油擎锋SUV|统一润滑油超粘王|统一润滑油经典AA|龙蟠音速T3|'
        '统一润滑油经典A2|长城金吉星J700|昆仑润滑油 润强|昆仑润滑油 润盛|昆仑润滑油 润福|美孚/Mobil MT80|长城SN5w30|长城 SN5w30|长城SN5W30|长城 SN5W30|长城润滑油官方正品C2/SP 0W30|'
        '长城润滑油官方正品C5/SP 0W20|A3B4/SN5W40|A3B4/SN 5W40|壳牌/Shell 蓝标|壳牌 蓝标|壳牌蓝标|壳牌/Shell蓝标|壳牌/Shell 银标|壳牌/Shell银标|壳牌银标|壳牌 银标|壳牌/Shell 金标|壳牌/Shell金标|'
        '壳牌金标|壳牌 金标|壳牌鹏致/PENNZOIL P7 Pro|壳牌鹏致/PENNZOIL N7|壳牌鹏致/PENNZOIL P9 Pro|壳牌鹏致/PENNZOIL Max 10|昆仑天驰 顺驰|昆仑天驰 劲驰|美孚/Mobil MT100|长城润滑油【勇】|'
        '长城润滑油【行】|壳牌机油Hx5Plus|壳牌鹏致/PENNZOIL P8 Pro|壳牌机油HX7p|HX7PLUS蓝壳|HX5PLUS黄壳|紫壳|勇 SP/GF-6A|美孚速霸节能保护|美孚1号劲擎表现',
        re.IGNORECASE)

    data_cc['model1'] = list(
        map(lambda x: pattern.search(x).group() if pd.notna(x) and pattern.search(x) != None else np.nan, data_cc[col]))
    # data_cc['model1'] = list(map(lambda x: ','.join(list(set(pattern.findall(x)))) if pd.notna(x) and pattern.search(x) != None else np.nan, data_cc[col]))

    dic1 = {'壳牌 超凡喜力 全合成机油 都市光影版': '壳牌超凡喜力都市光影', '途虎专供sp产品，取代以前的黑美': '美孚1号-黑金版',
            '壳牌爱德王子摩托车机油天然气全合成 ultra plus': '壳牌爱德王子ULTRA PLUS', '壳牌爱德王子摩托车机油天然气全合成ultra plus': '壳牌爱德王子ULTRA PLUS',
            '壳牌爱德王子摩托车机油润滑油天然气全合成': '壳牌爱德王子ULTRA PLUS', '壳牌爱德王子合成技术机油摩托车润滑油机油ax7': '壳牌爱德王子AX7',
            '壳牌爱德王子摩托车润滑油摩托车机油矿物质油ax3': '壳牌爱德王子AX3', '壳牌先锋超凡喜力欧系 千里江山': '壳牌先锋超凡喜力千里江山版',
            '壳牌先锋超凡喜力欧系千里江山版': '壳牌先锋超凡喜力千里江山版', '壳牌爱德王子合成技术机油摩托车润滑油机油ax5': '壳牌爱德王子AX5',
            '壳牌爱德王子高性能润滑油摩托车油踏板车机油ax5': '壳牌爱德王子AX5', '壳牌 喜力全合成机油 hx7 plus': '壳牌喜力HX7 PLUS',
            '美孚1号5w-40(经典系列)': '美孚一号金装 经典表现', '美孚1号 5w-40(经典系列)': '美孚一号金装 经典表现', '美孚1号5w-40 (经典系列)': '美孚一号金装 经典表现',
            '美孚1号 5w-40 (经典系列)': '美孚一号金装 经典表现', '壳牌极净超凡喜力千里江山': '壳牌极净超凡喜力千里江山版', '壳牌零碳环保恒护超凡喜力': '壳牌零碳环保恒护超凡喜力',
            '美孚1号5w-30静逸款': '美孚1号静逸', '新速霸1000合成机油': '美孚新速霸1000-每日保护', '美孚1号经典表现': '美孚一号金装 经典表现',
            '美孚黑霸王齿轮油85w-140': '美孚黑霸王齿轮油', '喜力全合成机油hx7 plus': '壳牌喜力HX7 PLUS', '喜力合成技术润滑油 hx5 plus': '壳牌喜力HX5 Plus',
            '喜力合成技术润滑油 hx5': '壳牌喜力HX5', '美孚1号 黑金版经典系列': '美孚1号黑美', '壳牌鹏致pennzoil p8 pro': '壳牌鹏致P8 Pro',
            '壳牌鹏致pennzoil p9 pro': '壳牌鹏致P9 Pro', '壳牌鹏致pennzoil cp8': '壳牌鹏致CP8', '壳牌 喜力半合成机油hx7': '壳牌喜力HX7',
            '壳牌鹏致pennzoil ep9': '壳牌鹏致EP9', '壳牌鹏致pennzoil n7': '壳牌鹏致N7', '壳牌鹏致pennzoil p7 pro': '壳牌鹏致P7 Pro',
            '壳牌鹏致pennzoil p7': '壳牌鹏致P7', '壳牌零碳先锋超凡喜力': '壳牌先锋超凡喜力', '壳牌锐净超凡喜力零碳': '壳牌锐净超凡喜力-零碳环保',
            '壳牌鹏致pennzoil sp7': '壳牌鹏致SP7', '美孚1号 5w-30涡轮增压': '美孚1号涡轮增压', '美孚1号5w-30涡轮增压': '美孚1号涡轮增压',
            '美孚1号5w-30 涡轮增压': '美孚1号涡轮增压', '壳牌超凡喜力 千里江山': '壳牌先锋超凡喜力千里江山版', '美孚1号长效款机滤': '美孚1号长效机滤',
            '美孚1号 0w-20混合动力': '美孚一号 定制表现', '美孚1号0w-20混合动力': '美孚一号 定制表现', '美孚1号0w-20 混合动力': '美孚一号 定制表现',
            '美孚一号定制系列混合动力': '美孚一号 定制表现', '美孚1号定制系列混合动力': '美孚一号 定制表现', '美孚1号 混合动力': '美孚一号 定制表现',
            '美孚速霸1000每日保护': '美孚新速霸1000-每日保护', '途虎专供sp': '壳牌超凡喜力-高效动力', '极净超凡喜力': '壳牌极净超凡喜力', '嘉实多 引擎洁霸': '嘉实多引擎洁霸',
            '新速霸1000': '美孚新速霸1000-每日保护', '速霸1000': '美孚速霸1000', '壳牌 施倍力 s6': '壳牌施倍力S6', '黄壳hx6': '壳牌喜力HX6',
            '黄壳hx5 plus': '壳牌喜力HX5 PLUS', '黄壳hx5': '壳牌喜力HX5', '蓝壳hx7 plus': '壳牌喜力HX7 PLUS', '蓝壳hx7': '壳牌喜力HX7',
            '蓝壳hx7': '壳牌喜力HX7', '壳牌 施倍力 s3': '壳牌施倍力S3', '壳牌 施倍力 s5': '壳牌施倍力S5', '美孚1号经典': '美孚一号金装 经典表现',
            '途虎的银美': '美孚1号-风尚版', '途虎专供': '美孚1号黑美', '途虎速霸2000': '美孚速霸-畅途版', '途虎速霸1000': '美孚速霸-安途版', '美孚 mt80': '美孚MT80',
            '嘉实多 超嘉护超净': '嘉实多超嘉护', '美孚 新速霸2000': '美孚速霸2000', '嘉实多 金嘉护': '嘉实多金嘉护', '嘉实多 超嘉护': '嘉实多超嘉护',
            '美孚1号 5w-40动逸': '美孚1号动逸', '美孚1号5w-40动逸': '美孚1号动逸', '美孚1号5w-40 动逸': '美孚1号动逸', '风尚版': '美孚1号-风尚版',
            '美孚1号 长里程': '美孚1号长里程', '美孚1号 涡轮增压': '美孚1号涡轮增压', '壳牌鹏致 p9 pro': '壳牌鹏致P9 Pro', 'classic sp': '美孚一号金装 经典表现',
            '超凡喜力': '壳牌超凡喜力', 'sp产品': '壳牌极净超凡喜力-零碳环保', 'sp产品': '壳牌超凡喜力-零碳环保', '力霸9000': '美孚力霸', '力霸特级': '美孚力霸',
            '黑霸王长效': '美孚黑霸王长效CK-4', '红壳hx3': '壳牌喜力HX3', '壳牌喜力 hx 6': '壳牌喜力HX6', '壳牌喜力 hx6': '壳牌喜力HX6',
            '壳牌 施倍力 s4': '壳牌施倍力S4', '壳牌施倍力 s4': '壳牌施倍力S4', '壳牌 施倍力s4': '壳牌施倍力S4', '嘉实多磁护suv': '嘉实多磁护SUV',
            '速霸全效保护': '美孚速霸全效保护', '美孚1号 动逸': '美孚1号动逸', '超劲活能': '嘉实多超劲活能', '速霸2000': '美孚速霸2000', '润滑脂mp': '美孚润滑脂MP',
            '润滑脂xhp': '美孚润滑脂XHP222', 'ultimate': '美孚1号劲擎表现', 'ultimate': '美孚1号劲擎表现', '力霸9000': '美孚力霸9000',
            '力霸特级': '美孚力霸特级', '嘉实多 新磁护启停保': '嘉实多磁护启停保', '新磁护': '嘉实多磁护', '超级奔程': '嘉实多超级奔程', '速霸高性能': '美孚速霸高性能',
            '银美': '美孚1号', '恒护': '壳牌恒护超凡喜力', '先锋': '壳牌先锋超凡喜力', 'ld3': '壳牌劲霸LD3', 'ld4': '壳牌劲霸LD4', 'ld5': '壳牌劲霸LD5',
            'r2': '壳牌劲霸R2', 'r3': '壳牌劲霸R3', 'r4': '壳牌劲霸R4', 'r5': '壳牌劲霸R5', 's2': '壳牌施倍力S2', 's2': '壳牌施倍力S2',
            's3': '壳牌施倍力S3', 's4': '壳牌施倍力S4', '极净': '壳牌极净超凡喜力', '极护': '嘉实多极护', '磁护': '嘉实多磁护', '金美0w': '美孚1号金美',
            '老速霸': '美孚速霸2000', '光影': '壳牌超凡喜力都市光影', '力霸': '美孚力霸', '灰壳': '壳牌超凡喜力', '超霸': '嘉实多超霸', '路宝gx': '美孚路宝车用齿轮油GX',
            '蓝壳喜力hx7plus': '壳牌喜力HX7 PLUS', '黄壳喜力hx5 plus': '壳牌喜力HX5 PLUS', '黄壳 helix hx5 plus': '壳牌喜力HX5 PLUS',
            'helix hx7 plus': '壳牌喜力HX7 PLUS', 'helix hx8 plus': '壳牌喜力HX8 PLUS', '蓝壳喜力hx7 plus': '壳牌喜力HX7 PLUS',
            'pennzoil p8 pro': '壳牌鹏致P8 Pro', 'pennzoil p9 pro': '壳牌鹏致P9 Pro', 'pennzoil p7 pro': '壳牌鹏致P7 Pro',
            '喜力 hx7 plus': '壳牌喜力HX7 PLUS', '喜力 hx7 plus': '壳牌喜力HX7 PLUS', '壳牌 hx5plus': '壳牌喜力HX5 Plus',
            '喜力hx5plus': '壳牌喜力HX5 Plus', '黄壳喜力hx5': '壳牌喜力HX5', '红壳喜力hx3': '壳牌喜力HX3', '黄壳helix hx6': '壳牌喜力HX6',
            'helix hx5': '壳牌喜力HX5', 'helix hx3': '壳牌喜力HX3', 'helix hx6': '壳牌喜力HX6', '白壳喜力hx2': '壳牌喜力HX2',
            '壳牌鹏致/sp7': '壳牌鹏致SP7', '壳牌鹏致/ep9': '壳牌鹏致EP9', '壳牌施倍力自动变速箱油全合成润滑油 s6': '壳牌施倍力S6',
            '壳牌施倍力无级变速箱油全合成润滑油 s5': '壳牌施倍力S5', '施倍力 s6': '壳牌施倍力S6', 'pennzoil max 10': '壳牌鹏致MAX10', '喜力hx6': '壳牌喜力HX6',
            '焕耀': '壳牌超凡喜力-焕耀版', 'hx5plus喜力': '壳牌喜力HX5 Plus', '超凡灰喜力': '壳牌极净超凡喜力-零碳环保', 'mobil mt80': '美孚MT80',
            '金美孚': '美孚1号金美', '金装美孚': '美孚1号金美', '银美孚一号': '美孚1号银美', '旋风超级4t': '美孚旋风4T', '嘉实多正品超嘉护': '嘉实多超嘉护',
            '金嘉护': '嘉实多金嘉护', '银嘉护': '嘉实多银嘉护', '超嘉护': '嘉实多超嘉护', '黑霸王': '美孚黑霸王', '金吉星 j700': '金吉星J700',
            '行 a3b4/sn': '长城金吉星行系列', '行 sp/gf-6a': '长城金吉星行系列', 'sonic 9000': '龙蟠SONIC9000', 'sonic t1': '龙蟠SONIC T1',
            'sonic t3': '龙蟠SONIC T3', 'sonic7000': '龙蟠SONIC7000', 'sonic9000': '龙蟠SONIC9000',
            '超速龙极致金牌sae5w-30/40bba适用': '龙蟠Trisonic', '净威a1': '龙蟠净威', '净威h1': '龙蟠净威', '净威k8': '龙蟠净威', '净威k9': '龙蟠净威',
            '龙蟠9000': '龙蟠SONIC9000', '龙蟠n1': '龙蟠SONIC N1', '龙蟠t1': '龙蟠SONIC T1', '龙蟠机油f1': '龙蟠SONIC F1',
            '龙蟠机油t1': '龙蟠SONIC T1', '四季通用sonic n1': '龙蟠SONIC N1', '四季通用sonic9000': '龙蟠SONIC9000', '音速t3': '龙蟠SONIC T3',
            '智尊a2': '龙蟠智尊', '智尊h2': '龙蟠智尊', '超粘王': '统一润滑油超粘王', '经典a0': '统一润滑油经典A0', '经典a1': '统一润滑油经典A1',
            '经典a2': '统一润滑油经典A2', '经典a3': '统一润滑油经典A3', '经典aa': '统一润滑油经典AA', '经典系列a0': '统一润滑油经典A0', '莫托维克': '统一润滑油莫托维克',
            '擎锋3000': '统一润滑油擎锋3000', '擎锋4000': '统一润滑油擎锋4000', '擎锋m3000': '统一润滑油擎锋M3000', '擎锋m5000': '统一润滑油擎锋M5000',
            '擎锋m5000': '统一润滑油擎锋M5000', '擎锋suv': '统一润滑油擎锋SUV', '神行者': '统一润滑油神行者', '统一（monarch）德国大众原厂认证汽机油': '统一润滑油OEM',
            '统一（monarch）京保养': '统一润滑油京保养', '统一润滑油官方旗舰 oem': '统一润滑油OEM', '新经典a3': '统一润滑油经典A3',
            '统一润滑油全合成机油汽车发动机油sn级': '统一润滑油', '统一润滑油全合成5w-40sn级1l*4汽车机油大众斯柯达通用': '统一润滑油', '统一润滑油官方旗舰 爱拼才会赢': '统一润滑油',
            '昆仑润滑0w-40润盛': '昆仑润盛', '昆仑润滑gl': '昆仑GL', '昆仑润滑车掌柜': '昆仑车掌柜', '昆仑润滑润福': '昆仑润福', '昆仑润滑润盛': '昆仑润盛',
            '昆仑润滑天润': '昆仑天润', '昆仑润滑天润润福': '昆仑润福', '昆仑润滑天润润强': '昆仑润强', '昆仑润滑天润润威': '昆仑润威', '昆仑润滑天威': '昆仑天威',
            '昆仑润滑天蝎sj': '昆仑天蝎SJ', '昆仑润滑油 京保养': '昆仑润滑油', '昆仑润滑油润福': '昆仑润福', '昆仑润滑油润强': '昆仑润强', '昆仑润滑油润盛': '昆仑润盛',
            '昆仑润滑油润威': '昆仑润盛', '昆仑润滑油天润': '昆仑天润', '昆仑润滑油天威': '昆仑天威', '昆仑润滑油天蝎': '昆仑天蝎SJ', '昆仑润滑油天蝎sj': '昆仑天蝎SJ',
            '昆仑润强全合成高性能': '昆仑润强', '昆仑天润': '昆仑天润', '昆仑小保养': '昆仑润滑油', '天工': '昆仑天工', '天威': '昆仑天威', '天蝎': '昆仑天蝎SJ',
            '快驰 ineo': '道达尔快驰 INEO', '快驰4000': '道达尔快驰4000', '快驰5000': '道达尔快驰5000', '快驰7000': '道达尔快驰7000',
            '快驰8000': '道达尔快驰8000', '快驰9000': '道达尔快驰9000', '经典系列classic 9': '道达尔经典系列CLASSIC 9', '能源快驰9000': '道达尔快驰9000',
            '道达尔机油 经典系列classic 9': '道达尔经典系列CLASSIC 9', '金吉星j700': '长城金吉星J700', 'pennzoil n7': '壳牌鹏致N7',
            '行 c3/sn': '长城金吉星行系列', '喜力hx7plus': '壳牌喜力HX7 PLUS', '金吉星【j700】': '长城金吉星J700', '【j700】金吉星': '长城金吉星J700',
            'sn 0w-40 全合成汽油机油 润滑油正品【干】': '长城金吉星干系列', '统一机油汽车小保养套餐': '统一润滑油', '壳牌机油大保养套餐': '壳牌润滑油', '昆仑那兔联名版': '昆仑润滑油',
            't1系列整箱4桶起售': '龙蟠SONIC T1', '昆仑润滑润强sn': '昆仑润强', '壳牌喜力hx7plus': '壳牌喜力HX7 PLUS', '昆仑润滑油 润强': '昆仑润强',
            '昆仑润滑油 润盛': '昆仑润盛', '昆仑润滑油 润福': '昆仑润福', '美孚/mobil mt80': '美孚MT80', '长城sn5w30': '长城金吉星行系列',
            '长城 sn5w30': '长城金吉星行系列', '长城sn5w30': '长城金吉星行系列', '长城 sn5w30': '长城金吉星行系列', '长城润滑油官方正品c2/sp 0w30': '长城金吉星干系列',
            '长城润滑油官方正品c5/sp 0w20': '长城金吉星干系列', 'a3b4/sn5w40': '长城金吉星行系列', 'a3b4/sn 5w40': '长城金吉星行系列',
            '壳牌鹏致/pennzoil p7 pro': '壳牌鹏致P7 Pro', '壳牌鹏致/pennzoil n7': '壳牌鹏致N7', '壳牌鹏致/pennzoil p9 pro': '壳牌鹏致P8 Pro',
            '壳牌鹏致/pennzoil max 10': '壳牌鹏致MAX10', '壳牌/shell 金标': '壳牌金标', '壳牌/shell金标': '壳牌金标', '壳牌 金标': '壳牌金标',
            '壳牌/shell 银标': '壳牌银标', '壳牌/shell银标': '壳牌银标', '壳牌 银标': '壳牌银标', '壳牌/shell 蓝标': '壳牌蓝标', '壳牌/shell蓝标': '壳牌蓝标',
            '壳牌 蓝标': '壳牌蓝标', '美孚mt100': '美孚/Mobil MT100', '长城润滑油【勇】': '长城金吉星勇系列', '长城润滑油【行】': '长城金吉星行系列',
            '锐净零碳全合成油': '壳牌锐净超凡喜力-零碳环保', '壳牌鹏致/max 10': '壳牌鹏致MAX10', '壳牌机油hx5plus': '壳牌喜力HX5 Plus',
            'hx7plus蓝壳': '壳牌喜力HX7 PLUS', '壳牌机油hx7p': '壳牌喜力HX7 PLUS', '壳牌鹏致/pennzoil p8 pro': '壳牌鹏致P8 Pro',
            '勇 sp/gf-6a': '长城金吉星勇系列',
            '美孚一号 定制表现': '美孚一号 定制表现', '美孚1号 定制表现': '美孚一号 定制表现', '美孚一号定制表现': '美孚一号 定制表现', '美孚1号定制表现': '美孚一号 定制表现',
            '美孚1号 劲擎表现': '美孚1号劲擎表现'}
    pattern1 = re.compile(
        '壳牌 超凡喜力 全合成机油 都市光影版|途虎专供SP产品，取代以前的黑美|壳牌爱德王子摩托车机油天然气全合成 ULTRA PLUS|壳牌爱德王子摩托车机油天然气全合成ULTRA PLUS|'
        '壳牌爱德王子摩托车机油润滑油天然气全合成|壳牌爱德王子合成技术机油摩托车润滑油机油AX7|壳牌爱德王子摩托车润滑油摩托车机油矿物质油AX3|壳牌先锋超凡喜力欧系 千里江山|'
        '壳牌先锋超凡喜力欧系千里江山版|壳牌爱德王子合成技术机油摩托车润滑油机油AX5|壳牌爱德王子高性能润滑油摩托车油踏板车机油AX5|壳牌 喜力全合成机油 HX7 Plus|'
        '美孚1号5W-40(经典系列)|美孚1号 5W-40(经典系列)|美孚1号5W-40 (经典系列)|美孚1号 5W-40 (经典系列)|壳牌极净超凡喜力千里江山|壳牌零碳环保恒护超凡喜力|美孚1号5W-30静逸款|'
        '新速霸1000合成机油|美孚1号经典表现|喜力全合成机油HX7 Plus|喜力合成技术润滑油 HX5 Plus|喜力合成技术润滑油 HX5|美孚1号 黑金版经典系列|壳牌鹏致PENNZOIL P8 Pro|'
        '壳牌鹏致PENNZOIL P9 Pro|壳牌鹏致PENNZOIL CP8|壳牌 喜力半合成机油HX7|壳牌鹏致PENNZOIL EP9|壳牌鹏致PENNZOIL N7|壳牌鹏致PENNZOIL P7 Pro|壳牌鹏致PENNZOIL P7|'
        '壳牌零碳先锋超凡喜力|壳牌锐净超凡喜力零碳|壳牌鹏致PENNZOIL SP7|美孚1号 5W-30涡轮增压|美孚1号5W-30涡轮增压|美孚1号5W-30 涡轮增压|壳牌超凡喜力 千里江山|美孚1号 0W-20混合动力|'
        '美孚1号0W-20混合动力|美孚1号0W-20 混合动力|美孚1号长效款机滤|美孚1号 0W-20混合动力|美孚1号0W-20混合动力|美孚1号0W-20 混合动力|美孚1号 混合动力|美孚速霸1000每日保护|途虎专供SP|'
        '极净超凡喜力|嘉实多 引擎洁霸|新速霸1000|速霸1000|壳牌 施倍力 S6|黄壳HX6|黄壳HX5 PLUS|黄壳HX5|蓝壳HX7 PLUS|蓝壳HX7|壳牌 施倍力 S3|壳牌 施倍力 S5|美孚1号经典|途虎的银美|途虎专供|'
        '途虎速霸2000|途虎速霸1000|美孚 MT80|嘉实多 超嘉护超净|美孚 新速霸2000|嘉实多 金嘉护|嘉实多 超嘉护|美孚1号 5W-40动逸|美孚1号5W-40动逸|美孚1号5W-40 动逸|风尚版|美孚1号 长里程|'
        '美孚1号 涡轮增压|壳牌鹏致 P9 Pro|Classic SP|超凡喜力|SP产品|SP产品|力霸9000|力霸特级|红壳HX3|壳牌喜力 HX 6|壳牌喜力 HX6|壳牌 施倍力 S4|壳牌施倍力 S4|壳牌 施倍力S4|嘉实多磁护SUV|'
        '速霸全效保护|美孚1号 动逸|超劲活能|速霸2000|润滑脂MP|润滑脂XHP|ultimate|力霸9000|力霸特级|嘉实多 新磁护启停保|新磁护|超级奔程|速霸高性能|恒护|先锋|LD3|LD4|LD5|R2|R3|R4|R5|S2|S3|S4|'
        '极净|极护|磁护|金美0W|老速霸|光影|力霸|灰壳|超霸|路宝GX|蓝壳喜力HX7PLUS|黄壳喜力HX5 PLUS|黄壳 Helix HX5 PLUS|Helix HX7 PLUS|Helix HX8 PLUS|蓝壳喜力HX7 PLUS|pennzoil p8 pro|'
        'pennzoil p9 pro|pennzoil p7 pro|喜力 HX7 Plus|喜力 HX7 PLUS|壳牌 Hx5Plus|喜力HX5Plus|黄壳喜力HX5|红壳喜力HX3|黄壳Helix HX6|Helix HX5|Helix HX3|Helix HX6|白壳喜力HX2|'
        '壳牌鹏致/SP7|壳牌鹏致/EP9|壳牌施倍力自动变速箱油全合成润滑油 S6|壳牌施倍力无级变速箱油全合成润滑油 S5|施倍力 s6|pennzoil max 10|壳牌鹏致/Max 10|喜力HX6|焕耀|HX5Plus喜力|超凡灰喜力|'
        'mobil mt80|金美孚|银美孚一号|旋风超级4T|嘉实多正品超嘉护|金嘉护|银嘉护|超嘉护|黑霸王|金吉星J700|长城金吉星行系列|长城金吉星勇系列|长城金吉星干系列|长城金吉星劲系列|金吉星 J700|行 A3B4/SN|'
        '行 SP/GF-6A|SONIC 9000|SONIC T1|SONIC T3|SONIC7000|SONIC9000|超速龙极致金牌SAE5W-30/40BBA适用|净威A1|净威H1|净威K8|净威K9|龙蟠9000|龙蟠N1|龙蟠T1|龙蟠机油F1|龙蟠机油T1|四季通用SONIC N1|'
        '四季通用SONIC9000|音速T3|智尊A2|智尊H2|超粘王|经典A0|经典A1|经典A2|经典A3|经典AA|经典系列A0|莫托维克|擎锋3000|擎锋4000|擎锋M3000|擎锋M5000|擎锋SUV|神行者|统一（Monarch）德国大众原厂认证汽机油|'
        '统一（Monarch）京保养|统一润滑油官方旗舰 OEM|新经典A3|统一润滑油全合成机油汽车发动机油SN级|统一润滑油全合成5w-40SN级1L*4汽车机油大众斯柯达通用|统一润滑油官方旗舰 爱拼才会赢|昆仑润滑0W-40润盛|昆仑润滑GL|'
        '昆仑润滑车掌柜|昆仑润滑润福|昆仑润滑润盛|昆仑润滑天润|昆仑润滑天润润福|昆仑润滑天润润强|昆仑润滑天润润威|昆仑润滑天威|昆仑润滑天蝎SJ|昆仑润滑油 京保养|昆仑润滑油润福|昆仑润滑油润强|昆仑润滑油润盛|'
        '昆仑润滑油润威|昆仑润滑油天润|昆仑润滑油天威|昆仑润滑油天蝎|昆仑润滑油天蝎SJ|昆仑润强全合成高性能|昆仑天润|昆仑小保养|天工|天威|天蝎|快驰 INEO|快驰4000|快驰5000|快驰7000|快驰8000|快驰9000|'
        '经典系列CLASSIC 9|能源快驰9000|道达尔机油 经典系列CLASSIC 9|pennzoil n7|行 C3/SN|喜力HX7plus|金吉星【J700】|【J700】金吉星|SN 0W-40 全合成汽油机油 润滑油正品【干】|统一机油汽车小保养套餐|'
        '壳牌机油大保养套餐|昆仑那兔联名版|T1系列整箱4桶起售|昆仑润滑润强SN|壳牌喜力hx7plus|美孚一号 定制表现|美孚1号 定制表现|美孚一号定制表现|美孚1号定制表现|美孚1号 劲擎表现|金装美孚|美孚1号定制系列混合动力|'
        '美孚一号定制系列混合动力', re.IGNORECASE)

    data_cc['model2'] = list(
        map(lambda x: pattern1.search(x).group().lower() if pd.notna(x) and pattern1.search(x) != None else np.nan,
            data_cc[col]))

    # data_cc['model2'] = list(
    #     map(lambda x: ','.join(list(set(pattern1.findall(x)))) if pd.notna(x) and pattern1.search(x) != None else np.nan,
    #         data_cc[col]))
    data_cc['model2'] = list(map(lambda x: dic1[str(x)] if pd.notna(x) and dic1[str(x)] else np.nan, data_cc['model2']))
    data_cc['model1'] = list(map(lambda x, y: x if pd.notna(x) else y, data_cc['model1'], data_cc['model2']))
    data_cc.drop(columns=['model2'], inplace=True)

    pattern2 = re.compile('美孚1号|壳牌超凡喜力|壳牌极净超凡喜力|壳牌先锋超凡喜力|龙蟠1号')
    data_cc['model1'] = list(
        map(lambda x, y: pattern2.search(x).group() if pd.isna(y) and pd.notna(x) and pattern2.search(x) != None else y,
            data_cc[col], data_cc['model1']))

    pattern_y = re.compile('勇.*?金吉星|金吉星.*?勇|长城.*?勇|勇.*?长城')
    pattern_g = re.compile('干.*?金吉星|金吉星.*?干|长城.*?干|干.*?长城')
    pattern_j = re.compile('劲.*?金吉星|金吉星.*?劲|长城.*?劲|劲.*?长城')
    pattern_x = re.compile('行.*?金吉星|金吉星.*?行|长城.*?行|行.*?长城')
    pattern_ts = re.compile('昆仑.*?顺驰|天驰.*?顺驰|顺驰.*?昆仑')
    pattern_tj = re.compile('昆仑.*?劲驰|天驰.*?劲驰|劲驰.*?昆仑')
    pattern_d = re.compile('道达尔.*?经典.*?\d+')
    pattern_s = re.compile('SONIC.*?9000')
    pattern_q = re.compile('壳牌.*?蓝壳.*?[^PLUSplus]*?|壳牌.*?蓝喜力.*?[^PLUSplus]*?', re.IGNORECASE)
    pattern_r = re.compile('壳牌.*?锐净.*?')
    data_cc['model1'] = list(map(lambda x, y, z: '长城金吉星勇系列' if pd.notna(x) and y == '长城' and pattern_y.search(x) != None
    else ('长城金吉星干系列' if pd.notna(x) and y == '长城' and pattern_g.search(x) != None
          else ('长城金吉星劲系列' if pd.notna(x) and y == '长城' and pattern_j.search(x) != None
                else ('长城金吉星行系列' if pd.notna(x) and y == '长城' and pattern_x.search(x) != None
                      else ('昆仑天驰顺驰' if pd.notna(x) and y == '昆仑' and pattern_ts.search(x) != None
                            else ('昆仑天驰劲驰' if pd.notna(x) and y == '昆仑' and pattern_tj.search(x) != None
                                  else ('道达尔经典系列CLASSIC 9' if pd.notna(x) and y == '道达尔' and pattern_d.search(x) != None
                                        else ('龙蟠SONIC9000' if pd.notna(x) and y == '龙蟠' and pattern_s.search(x) != None
                                              else (
        '壳牌喜力HX7' if pd.notna(x) and y == '壳牌' and pattern_q.search(x) != None
        else ('壳牌锐净超凡喜力-零碳环保' if pd.notna(x) and y == '壳牌' and pattern_r.search(x) != None else z))))))))),
                                 data_cc[col], data_cc['keyword'], data_cc['model1']))

    data_cc[out_model] = data_cc['model1']
    data_cc.drop(['model1'], axis=1, inplace=True)
    return data_cc


# 水军判定
def waterStick(df):
    def isTimeContinuous(df, sum_count='count', time_move=1):

        sum_count = df[sum_count].sum()
        len_df = df.shape[0]
        if len_df <= 10:
            df['flag'] = 0
            df['flag_sj_1'] = '0'
            df['flag_sj_2'] = '0'
            df['flag_sj_3'] = '0'
            return df
        else:
            if time_move == 1:
                df['count_shift'] = df['count'].shift(1)
                df['count_shift_d'] = df['count'].shift(-1)
                df['time_shift'] = df['timestamp'].shift(1)
                df['time_shift_d'] = df['timestamp'].shift(-1)

                df['flag'] = list(map(lambda x, y, a, b: '0' if pd.isna(y) else ('0.2' if (int(eval(
                    x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(
                    eval(x + '-' + y)) == 77) and ((a - b) > (sum_count / len_df)) else '0'), df['timestamp'],
                                      df['time_shift'], df['count'], df['count_shift']))
                df['flag1'] = list(map(lambda x, y, a, b: '0' if pd.isna(x) else ('0.05' if (int(eval(
                    x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(
                    eval(x + '-' + y)) == 77) and ((b - a) > (sum_count / len_df)) else '0'), df['time_shift_d'],
                                       df['timestamp'], df['count_shift_d'], df['count']))
                df['flag'] = list(
                    map(lambda x, y: str(eval(x + '+' + '0.1')) if y > 2 * sum_count / len_df else x, df['flag'],
                        df['count']))
                df['flag'] = list(map(lambda x, y: eval(x + '+' + y), df['flag'], df['flag1']))

                df['flag_sj_1'] = list(map(lambda x, y, a, b: '0' if pd.isna(y) else ('0.2' if (int(eval(
                    x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(
                    eval(x + '-' + y)) == 77) and ((a - b) > (sum_count / len_df)) else '0'), df['timestamp'],
                                           df['time_shift'], df['count'], df['count_shift']))
                df['flag_sj_2'] = list(map(lambda x, y, a, b: '0' if pd.isna(x) else ('0.05' if (int(eval(
                    x + '-' + y)) == 1 or int(eval(x + '-' + y)) == 886977 or int(eval(x + '-' + y)) == 6977 or int(
                    eval(x + '-' + y)) == 77) and ((b - a) > (sum_count / len_df)) else '0'), df['time_shift_d'],
                                           df['timestamp'], df['count_shift_d'], df['count']))
                df['flag_sj_3'] = list(
                    map(lambda x, y: '0.1' if y > 2 * sum_count / len_df else '0', df['flag'], df['count']))

                df.drop(['flag1'], axis=1, inplace=True)

                # print(df[['timestamp', 'time_shift', 'count', 'count_shift', 'count_shift_d', 'flag']].head())
                # print(sum_count/len_df)
            else:
                pass
            return df

    def stdCountSum(df):
        std_count = np.std(df['count'])
        df['std_count'] = std_count

        return df

    return df


def splitSentenceUseSnownlp(df, col=''):
    pattern = re.compile('[,，.。;；！!？?]')
    df['avg_score'] = list(
        map(lambda x: sum([SnowNLP(i).sentiments for i in pattern.findall(x)]) / len(pattern.findall(x)) if pd.notna(
            x) and pattern.search(x) != None else SnowNLP(x).sentiments, df[col]))

    return df


def addNewWords(path='../data/wordDic/addName.txt'):
    addwords = [line.strip() for line in open(path, encoding='UTF-8').readlines()]
    for i in addwords:
        jieba.add_word(i)


def get_stopwords_list(path='../data/wordDic/mainStopWord.txt'):
    stopwords = [line.strip() for line in open(path, encoding='UTF-8').readlines()]
    return stopwords


def move_stopwords(sentence_list, stopwords_list):
    # 去停用词
    out_list = []
    for word in sentence_list:
        # if word not in stopwords_list and len(word) > 1:
        if word not in stopwords_list:
            if not remove_digits(word):
                continue
            if word != '\t':
                out_list.append(word)
    return out_list


def remove_digits(input_str):
    punc = u'0123456789.'
    output_str = re.sub(r'[{}]+'.format(punc), '', input_str)
    return output_str


def drop_wan_to_num(strings):

    pattern = re.compile('万')
    if pattern.search(strings):
        strings = str(eval(pattern.sub('', strings) + '*10000'))

    return strings

