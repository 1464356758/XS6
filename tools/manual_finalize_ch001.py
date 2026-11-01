#!/usr/bin/env python3
"""One-shot author-approved CH001 file-tools execution. No model or platform publishing."""
from pathlib import Path
import json, os, subprocess, sys, hashlib, datetime

ROOT=Path(".")
BOOK=Path("book")
DRAFT=Path("drafts/CH001.txt")
IDENTITY="d3639881-8d19-4090-9daf-f2ac7a1048f3"

def run(script,*args):
    cmd=[sys.executable,"tools/"+script,*args]
    r=subprocess.run(cmd,text=True,capture_output=True,timeout=90)
    print("$", " ".join(cmd), "\n",r.stdout[-10000:],r.stderr[-3000:],flush=True)
    if r.returncode:
        raise RuntimeError("File tool failure: "+str(cmd))
    return r.stdout

def write(path,data):
    path=Path(path)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def check_quote(body,quote):
    if not quote or quote not in body:
        raise RuntimeError("Evidence quote not found: "+str(quote))
    return quote

def ev(body,quote,sha):
    return {"chapter":1,"sha256":sha,"quote":check_quote(body,quote)}

def main():
    import sys as pysys
    pysys.path.insert(0,"tools")
    import novel_state as ns
    state=json.loads((BOOK/"state.json").read_text(encoding="utf-8"))
    if state["book_id"]!=IDENTITY or len(state["chapters"])!=0 or state["revision"]!=5 or state["tasks"]:
        raise RuntimeError("Existing state changed: do not reset or overwrite")
    if json.loads((BOOK/"workflow.json").read_text(encoding="utf-8"))["phase"]!="REVIEWING":
        raise RuntimeError("Workflow stage changed")
    body=DRAFT.read_text(encoding="utf-8")
    digest=hashlib.sha256(body.encode("utf-8")).hexdigest()
    if digest!="911ddc4711d3c0fef9ff621031761eeef8b4838ae27cf5981ef7e49c57cc75f3":
        raise RuntimeError("Chapter text SHA changed")
    assert 8000<=ns.han_count(body)<=10000
    assert ns.han_count(body[:body.index("系统提示：封存异常已登记")])<=2600

    briefpath="drafts/CH001_brief_request.json"
    run("novel_state.py","--root","book","brief-request","--out",briefpath)
    brief=json.loads(Path(briefpath).read_text(encoding="utf-8"))
    brief.update(decision="ready",
      writer_brief="林砚秋在灰霾时分带九岁患哮喘的女儿到穹顶一号，因医疗需求风险标签遭拒。她先寻求现实复核，失败后在2600汉字内实际破坏U-07公共机组的封存并留下实名痕迹。她未得到机器，仍然没有新风源，还要面对自己可能影响其他人的责任。不能轻易洗白，也不能用管理员反派化替代真实稀缺；刻画女儿有观察与发问能力，突出母女爱与不被允许隐瞒的道德债。",
      hard_boundaries=[
        "U-07为近两百公斤的公共机组；一人不能搬运，章末仍在A区。",
        "风机过滤并不产生氧气，滤芯不能无代价去除全部毒气，真实气体读数未知。",
        "行政高医疗需求风险标签不是医学诊断；女儿的病不是传染病。",
        "母亲不知道机组受影响的确切人群；女儿更不可能提前知道下游具体后果。",
        "故事发生于2041年9月18日清晨，前800汉字内拒收，2600汉字内有真实违约行动。",
        "不复制其他小说；正文只呈现人物在场可知的事实，不使用生产标签。"
      ],
      reader_promise="母亲为一个孩子跨越公产边界，立即付出职业与信誉代价，但机器仍然搬不走；使读者既希望她救下女儿，也担心别人因此失去救援。",
      history_queries=[],
      scene_plan=[
        {"purpose":"灰霾到来，母女在门外被拒，女孩质问为何名字灰了。","target_han":650},
        {"purpose":"现场申诉失败，显示行政筛检与医学评估不同。","target_han":800},
        {"purpose":"母亲查U-07并实际破坏封存，留下实名记录和代价。","target_han":1150},
        {"purpose":"值守唐识反对，维护资格被停，母女互相追问。","target_han":1650},
        {"purpose":"寻找救济与运输路，顺手帮助另一位母亲找到凭证，孩子病况需医护评估。","target_han":2300},
        {"purpose":"运载路线封闭，地铁旧调度线索出现，母女带着责任与未知离开队列。","target_han":2450}
      ])
    write(briefpath,brief)
    run("novel_state.py","--root","book","brief-check","--file",briefpath)
    run("novel_state.py","--root","book","history-search","--query","林砚秋 设备 封签")
    run("novel_state.py","--root","book","context","--profile","writer","--out","drafts/CH001_writer_packet.md")
    run("novel_state.py","--root","book","candidate","--chapter","1","--text",str(DRAFT))
    textsha=digest
    fact_data=[
      ("state","entry:child","林知禾被穹顶一号暂缓接收。","",7,"状态：暂缓接收。"),
      ("knowledge","P02:denial","林知禾知道自己被拒，却不知道真实评分原因。","P02",7,"“那我的名字为什么是灰的？”"),
      ("fact","U07:asset","U-07是公有救灾设备，初始标识备用待分配。","",16,"标着U-07。"),
      ("fact","U07:breached","林砚秋已经破坏U-07封存纸带并被实名记录。","",16,"系统提示：封存异常已登记。操作人，林砚秋。原设备授权状态不可自行恢复。"),
      ("state","P01:maintenance_authorization","林砚秋维护权限与临时工位资格被暂停。","",24,"维护权限暂停的通知正式到达"),
      ("knowledge","P01:downstream","林砚秋不知道U-07确切分配给谁，承认不能把待分配当作无人需要。","P01",16,"一张没有最终去向的记录，不等于没有人正等着它。"),
      ("state","P02:medical_observation","林知禾经户外护士初步观察，不等于正式床位接收。","",69,"护士给她一张带时间的临时观察条"),
      ("fact","A:access:vehicle","A区库房升降台停用，通向外面的坡道也已封闭。","",80,"可升降台今天停了。"),
      ("fact","U07:location:end","截至章末U-07设备仍在A区受控区域，没有运到河湾。","",122,"那台近两百公斤的设备仍锁在受控区域"),
      ("fact","WuJing:family:reentry","伍静凭补查手写登记恢复再入内核验，孩子床位没有变化。","",80,"孩子在，床位未变，监护人被误录成临时离开")
    ]
    facts=[{"kind":kind,"key":key,"value":value,"holder":holder,"valid_from":start,"valid_until":None,"quote":check_quote(body,quote)}
            for kind,key,value,holder,start,quote in fact_data]
    events=[
      {"id":"K01","action":"plant","description":"女儿被行政高医疗需求风险标签拒收，评分依据尚未查实。","quote":check_quote(body,"原因：高医疗需求风险。")},
      {"id":"K02","action":"plant","description":"U-07公共备用机组存在未知下游受益者，女主的夺机行为可能让其他人失去保障。","quote":check_quote(body,"一张没有最终去向的记录，不等于没有人正等着它。")},
      {"id":"K03","action":"plant","description":"旧地铁能否成为合格避难空间仍未知，机器尚无合法接收点与进排风路径。","quote":check_quote(body,"有名字的地方，不等于可以活命的地方。")}
    ]
    record={
      "chapter":1,"title":"门外还有一个孩子","stage":"S01","base_revision":state["revision"],
      "canon_sha256":state["inputs"]["canon"]["sha256"],"text_sha256":digest,"complete":True,
      "story_time_end":122,
      "summary":"2041年9月18日，林砚秋带女儿林知禾到穹顶一号，知禾因行政高医疗需求风险被拒。母亲未能获得及时复核，为争取生存选择破坏公有U-07机组封存并留下实名记录。维护资格遭暂停，机组仍留A区。她在门外协助伍静找回入站证明，女儿接受临时观察；唐识提供已公开的转运示意信息，指出设备转运路径封闭，旧七号线可能是另一个方向但尚未实测。章末母亲承担盗机风险与未知下游责任，第二章须先解决机械搬运和地下空间安全。",
      "review":{"read_full_text":True,"decision":"adopt","blocking_issues":[],"sources_checked":[],
                "conclusion":"对正文逐场复核：实际越界在第3000汉字前；9000余汉字的场景含拒收、未获批改动、唐识对立、伍静证据救济、护士观察与转运障碍。未把外部调拨后果假设成已证实伤亡。读者同上下文近似审读，仍须关注下一章实际物流与气体安全。"},
      "facts":facts,
      "progression":{
        "goal":"在越来越危险的外部空气中为知禾争取可以呼吸的地方。",
        "obstacle":"行政风险配额拒收、复核迟缓、设备公产归属、现实无转运或接收空间。",
        "method":"先申诉，再冒险触碰公产封存，随后寻找可核的转运信息和医护照护。",
        "choice":"自行破坏U-07封存，承担可追责的设备管理风险；后来公开承认行为而不谎称已获批准。",
        "result":"母女仍未入站，机组仍在受控区；但女主获得有限路况线索，伍静的监护登记也被补正。",
        "consequence":"维护权限暂停，设备调拨暂停受核，孩子对母亲产生新疑虑，其他机组受益者身份未知。",
        "next_options":"调查七号线河湾站实际状况，寻找周闻笙与合格运载工具，核对U-07完整调度归属。",
        "scene_function":"拒收钩子、母女自主互动、可追责越界、次级救助对照、技术与责任长线。"},
      "thread_events":events,"stage_closing":False}
    recordpath="drafts/CH001_record.json";write(recordpath,record)
    run("novel_state.py","--root","book","check-record","--text",str(DRAFT),"--record",recordpath)
    run("novel_state.py","--root","book","context","--profile","reader","--text",str(DRAFT),"--out","drafts/CH001_reader_packet.md")
    reportpath="drafts/CH001_release_report.json"
    run("novel_state.py","--root","book","release-request","--text",str(DRAFT),"--record",recordpath,"--out",reportpath)
    report=json.loads(Path(reportpath).read_text(encoding="utf-8"))
    report.update(
       decision="release",read_full_text=True,blocking_issues=[],
       reader_reason_to_continue="女儿仍没获得正式收容，U-07仍被锁在库房，前往旧地铁的坡道封闭；母亲损害未知的其他病人保障，读者必须知道她能否真的把设备搬走以及如何承担责任。",
       consequence="封存异常实名留痕、母亲维修许可被停、U-07暂停调拨，女儿与母亲第一次明确讨论盗机可能伤害他人。",
       ending_runway="剩99章约90万字的总路线中，第二章实际运输，第三章独立风道，第四章电池底线均未提前解决。")
    category_review={
      "timeline":("九月十八日早晨六点零七分","从06:07拒收、06:23留痕到08:02退出队列，整体正向时间无提前知情。"),
      "knowledge":("一张没有最终去向的记录，不等于没有人正等着它。","女主只知台账待分配，不知受损者；知禾只见母亲碰公产，未知下游；不存在上帝视角提前定罪。"),
      "props_resources":("支架、管件、电池和机组加起来接近两百公斤","设备仅破封尚未搬走，未凭空产生氧气、电力、车辆或可用滤材；药物剂量没有虚构。"),
      "causality":("系统提示：封存异常已登记。操作人，林砚秋。原设备授权状态不可自行恢复。","主角自行撕封签后系统留名，唐识上报、工位停权、设备被暂停调拨，动作带来可见代价。"),
      "power_rules":("你是设备维修员，不是调拨员。","维护工权不能替代公共调度权，唐识有正当反对理由，女孩的医学标签不等于传染诊断。"),
      "promises":("受影响的保障安排","K01拒收原因、K02下游利益、K03旧地铁安全均有实际植入并明确后续兑现章，未假装谜团已经解决。"),
      "anti_repeat":("找簿子花了六分钟","首章没有旧章可以对比，伍静用纸质证据改正登记和主角偷机形成不同取舍，不连续重复争吵。"),
      "character_agency":("她却按下了提交","母亲明确选择跨线并面对代价；孩子主动帮助人、质问母亲，唐识与护士各自执行有边界的职责。")
    }
    for key,(quote,conclusion) in category_review.items():
      report["checks"][key]={"decision":"pass","conclusion":conclusion,"evidence":[ev(body,quote,digest)]}
    future={
      2:("找到合法可走的机械运输线并联络有旧轨道权限的人。","让母亲的违规从封存问题升级为实际运载与合作条件。","设备离开A区后究竟能在哪里运行？"),
      3:("在地下隔间建立有排风路径和独立读数的新风方案。","从拿到设备变成认识污染入侵与二氧化碳边界。","通风可靠却能运行多久？"),
      4:("实测电池与照明等综合负荷，安排第一夜的用电。","耗能和容量决定谁可临时进入，医护拥有真实判断权。","当额外求助者到来时该把谁拒之门外？")
    }
    for item in report["future_window"]:
      item.update(goal=future[item["chapter"]][0],change=future[item["chapter"]][1],ending_question=future[item["chapter"]][2])
    report["opening"]={
      "first_hook":{"quote":check_quote(body,"状态：暂缓接收。"),"why":"第一屏以九岁儿童被拒收引出明确冲突，位置在开篇800字内。"},
      "core_promise":{"quote":check_quote(body,"系统提示：封存异常已登记。操作人，林砚秋。原设备授权状态不可自行恢复。"),"why":"题材卖点不是空口计划，母亲在3000汉字内实际破坏公产封存并留下实名痕迹。"},
      "protagonist_impact":{"quote":check_quote(body,"她只是把自己从一个申请帮助的母亲，变成了第一责任栏上有名字的人。"),"why":"选择改变其法律和职业处境且不能撤销，发生在3000汉字内。"}
    }
    deadlines={"K01":10,"K02":16,"K03":10}
    for item in report["promise_reviews"]:
      item.update(action="set",deadline_chapter=deadlines[item["id"]],
                  reason={"K01":"第一章只看到行政标签，需CH010首次核查依据；模型全因果以后逐步揭示。",
                          "K02":"只有可能受影响的公共备用需求，CH016核实第一批真实下游后果。",
                          "K03":"旧地铁尚无实测，CH003证明有限净化空间，CH010完成首周临时安全框架。"}[item["id"]],
                  evidence=ev(body,{"K01":"原因：高医疗需求风险。","K02":"一张没有最终去向的记录，不等于没有人正等着它。","K03":"有名字的地方，不等于可以活命的地方。"}[item["id"]],digest))
    nr=report["narrative_review"]
    scene_specs=[
      ("闸机拒收九岁儿童","母亲没有先离开孩子，也没有接受行政标签就是诊断","读者即时理解风险与生存目标","状态：暂缓接收。"),
      ("复核无法在下轮空气评估前兑现","母亲仍求书面来源而非第一次就暴力冲关","合法救助的时效限制成为主动选择压力","二级复核，最早十点之后。"),
      ("维修库看到U-07且后续归属不清","母亲扯断封签并上传实名申请","公共设备封存和自身身份不可逆地受影响","系统提示：封存异常已登记。操作人，林砚秋。原设备授权状态不可自行恢复。"),
      ("值守唐识拒绝违规调拨","女主不砸通讯也不撒谎，承认自己行为","维护权暂停，权利边界被具体反驳","你是设备维修员，不是调拨员。"),
      ("母亲帮助伍静找回监护凭证","她选择实查纸账而非用被暂停的工牌施压","另一名母亲获得可核再入站凭证，但知禾仍未获得床位","孩子在，床位未变，监护人被误录成临时离开"),
      ("医护检查和调度路况双重受阻","母亲接受只能初评的护士判断，承认设备无法独自搬走","女儿有短时观察记录，U-07仍锁在A区，河湾成待核选项","那台近两百公斤的设备仍锁在受控区域")
    ]
    nr["actual_scenes"]=[{"event":e,"choice":c,"change":ch,"evidence":[ev(body,q,digest)]} for e,c,ch,q in scene_specs]
    nr["plan_comparison"]="六场核心方向兑现，但实际书面复核、伍静纸账和医护观察占篇幅比原计划更多；完整机械搬运有意识留到下一章，避免近200公斤设备被单人运走。"
    nr["reader"].update(mode="same_context_approximation",
       limitation="同一GPT写作与审读，已知道故事规划，不能冒称独立盲读或真实读者。",
       understanding="只从正文可得母女被拒、母亲冒险留痕、设备并未搬离、其他潜在受益者尚不明确。",
       information_load="技术词只在影响现场选择时出现；纸质凭证救援是第二种对照，不混同于女儿入站。",
       promise_delivery="标题所述拒收已落实，夺机实质冒险已发生，完整救援的代价尚未解除。",
       evidence=[ev(body,"她只是把自己从一个申请帮助的母亲，变成了第一责任栏上有名字的人。",digest)],
       issues=[])
    nr["character_causality"]={
      "opposition":{"status":"reviewed","conclusion":"唐识反对基于公产调拨与未明下游利益，不是单纯迫害母女；他仍提供公开路况。","evidence":[ev(body,"你是设备维修员，不是调拨员。",digest)]},
      "dialogue":{"status":"reviewed","conclusion":"知禾的问题体现九岁孩子对名字和危险的直觉，唐识坚持职责，母亲承认害怕且未为行为开脱。","evidence":[ev(body,"“妈妈，原来你也会害怕。”",digest)]},
      "aftermath":{"status":"reviewed","conclusion":"封签被撕后立即上报并停权，孩子出现具体怀疑，设备仍处受控区且暂停调拨，不以胜利抹除损失。","evidence":[ev(body,"维护权限暂停的通知正式到达",digest)]}
    }
    nr["history"].update(queries=[],comparisons=[],no_match_reason="本书第1章，正式已采用历史为0章；检查本章两类求援办法并非同桥段重复，无法凭空声称回查了旧章节。")
    nr["reader_updates"]=[
      {"kind":"observed","statement":"林知禾被A区风险评分暂缓接收。","evidence":[ev(body,"状态：暂缓接收。",digest)]},
      {"kind":"observed","statement":"林砚秋破坏封存实名留痕且维护许可暂停。","evidence":[ev(body,"系统提示：封存异常已登记。操作人，林砚秋。原设备授权状态不可自行恢复。",digest)]},
      {"kind":"uncertain","statement":"未知谁原本会使用U-07；可能存在因暂停调拨受损的其他人。","evidence":[ev(body,"一张没有最终去向的记录，不等于没有人正等着它。",digest)]},
      {"kind":"observed","statement":"章末U-07尚未从A区移出，旧线路运输路径未证明可用。","evidence":[ev(body,"那台近两百公斤的设备仍锁在受控区域",digest)]}
    ]
    nr["reader_update_note"]="只登记读者从第一章正文能确认的拒收、封存、停权、医护观察和设备位置；A区下游具体因果及河湾能否安全均保留为未知。"
    if nr["surface_findings"]:
      raise RuntimeError("Production language scan found items; revise prose instead of auto-clearing")
    write(reportpath,report)
    run("novel_state.py","--root","book","release-check","--text",str(DRAFT),"--record",recordpath,"--report",reportpath)
    run("novel_state.py","--root","book","adopt","--text",str(DRAFT),"--record",recordpath)
    run("online_state.py","--project",".","task","--phase","WAITING_NEXT","--detail","第001章《门外还有一个孩子》经实际文件工具release-check后采用并冻结；平台未登记发布。","--next","等作者授权续写下一章；前面冻结章绝不可更改。","--chapter","2")
    run("online_state.py","--project",".","build-index")
    run("online_state.py","--project",".","validate-index")
    final=json.loads((BOOK/"state.json").read_text(encoding="utf-8"))
    assert len(final["chapters"])==1 and final["serialization"]["frozen"]["1"]["text_sha256"]==digest
    assert not final["serialization"]["published"] and final["config"]["serial_mode"]
    write("drafts/CH001_local_verification.json",{
      "status":"chapter_adopted_locally","chapter":1,"body_sha256":digest,
      "han":ns.han_count(body),"source_book_id":IDENTITY,
      "review_mode":"same_context_approximation",
      "note":"This is a tool validation artifact. GitHub commit and remote readback are still required."
    })
    print("CH001_LOCAL_TOOL_PASS",digest,ns.han_count(body))

if __name__=="__main__": main()
