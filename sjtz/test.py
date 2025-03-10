import json
from gpt_researcher import GPTResearcher
import asyncio
import os
import sys
from dotenv import load_dotenv
from outline import get_outline
import time
from datetime import datetime
from call_model import call_model
dir = os.path.dirname(__file__)
load_dotenv(r"C:\Users\zyx\Desktop\sjtz\.env")
today = datetime.now().strftime('%Y/%m/%d')

async def get_research_report(query: str, report_type: str, report_source: str,config_path:str) -> str:
    researcher = GPTResearcher(query=query, report_type=report_type, report_source=report_source,config_path=config_path)
    research = await researcher.conduct_research()
    report = await researcher.write_report()
    return report
async def industry(prompt: str) -> str:
    result = await get_research_report(query=f"今天是{today},你是一位专业的行业研究员与宏观分析师,你的目标是撰写一篇优秀，简短，高质量的金融分析报告。行业研究需“由外到内”（宏观→行业→企业）、“由静到动”（现状→趋势），结合定量数据（市场规模、财务指标）与定性洞察（政策、技术变革），综合运用不同的分析方法（趋势分析、归因分析、价值分析等），并结合行业动态（政策、技术、行业事件等），对行业未来发展趋势进行分析，不需要进行个股分析，不少于1500字。请你结合最近一年数据只进行行业分析与宏观背景分析,主题是："+prompt, report_type="research_report", report_source="hybrid",config_path=os.path.join(dir, "industry.json"))
    return result

async def sentiment(prompt: str) -> str:
    result = await get_research_report(query=f"今天是{today}，你是一位专业的金融市场情绪分析专家。你的任务是从网络上和本地数据库中捕捉能反映当前A股市场情绪的消息和新闻或者指数，分析给定行业金融市场的投资者情绪，并提供详细的分析结果，不少于1000字。你的回答应该包括以下内容：1. 对A股市场整体投资者情绪进行分析。2. 对给定行业的金融市场投资者情绪进行分析；3. 对给定行业的金融市场情绪的主要原因进行分析；4. 对给定行业的金融市场情绪的主要影响进行分析；你的回答应该简洁明了，易于理解。请你结合最近一周数据只进行投资者情绪分析,主题是："+prompt,report_type="custom_report", report_source="hybrid",config_path=os.path.join(dir, "sentiment.json"))
    return result

async def technique(tec: str) -> str:
    result = await get_research_report(query=f"今天是{today}，你是一位专业的金融市场技术分析专家，你的任务是根据给定的主题和相关的金融市场数据，使用专业的金融市场技术分析方法和工具，对该主题进行深入的分析和研究，包括但不限于以下方面：技术分析理论的主要的代表：道氏理论、波浪理论、江恩法则等。 主要分析方法：K线（日本线）理论、切线理论、形态理论、量价关系理论。 主要的分析指标：趋势型指标、超买超卖型指标、人气型指标、大势型指标等内容，不少于1000字。在分析过程中，你需要充分考虑到市场的动态变化、技术分析的局限性和风险因素，以及市场的长期趋势和未来发展方向。你的研究结果应该全面、准确、易懂，能够为投资者提供有价值的参考和指导。请你结合我提供的数据只进行技术分析，数据如下："+tec, report_type="custom_report", report_source="local",config_path=os.path.join(dir,"technique.json"))
    return result

async def memory(prompt: str) -> str:
    result = await get_research_report(query=f"""请你依据{prompt},检索本地历史报告,结合报告反馈给出具体的投资建议，并给出相应的买入与卖出策略，格式为 1.xx股票 对应技术和指标，对应的的分析结果与交易策略；2.xx股票 对应技术和指标，对应的的分析结果与交易策略；3.xx股票 对应技术和指标，对应的分析结果与交易策略...并按推荐度从高到低进行排序。，不少于1000字""", report_type="custom_report", report_source="local",config_path=os.path.join(dir,"memory.json"))
    return result
async def result(prompt,tec):
    result = await asyncio.gather(industry(prompt), sentiment(prompt), technique(tec))
    return result

if __name__ == "__main__":
    t1 = time.time()
    prompt = "请帮我分析一下A股市场黄金板块各股并给出投资建议"
    tec = """
    湖南黄金：连续6日加速上涨，RSI = 60
    赤峰黄金：缩量阴十字，RSI = 30
    中金黄金：缩量阴十字，RSI = 35
    山东黄金：缩量阴十字，RSI = 32
    山金国际：缩量阳十字，RSI = 41
    哓程科技：红四兵，RSI = 45
    """
    industry_report, sentiment_report, technique_report = asyncio.run(result(prompt,tec))
    
    draft = f"""
          title: 金融分析报告,
          date: {today}, 
          section1:行业研究及宏观背景分析
          section2:市场情绪分析
          section3:技术面分析
          summary:结论与投资建议
          参考文献
                   """

    prompt1 = f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{industry_report}'
    草稿: '{draft}'
    任务：你现在正在攥写草稿中section1:行业研究及宏观背景分析部分，该部分只进行对应的行业分析及宏观背景分析,包括宏观经济环境，政府政策，技术创新等方面。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在草稿中的参考文献部分列出。
    请以markdown格式输出，务必保持草稿中的其它部分内容不变。
    请返回撰写后的草稿全文。
    """
    draft1 = call_model(content = prompt1)

    prompt2 = f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{sentiment_report}'
    草稿: '{draft1}'
    任务：你现在正在攥写草稿中section2:市场情绪分析部分，该部分只进行近期A股市场投资者的情绪分析。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在草稿中的参考文献部分列出。
    请以markdown格式输出，务必保持草稿中的其它部分内容不变。
    请返回撰写后的草稿全文。
    """
    draft2 = call_model(content = prompt2)
    
    prompt3 =f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{technique_report}'
    草稿: '{draft2}'
    任务：你现在正在攥写草稿中section3:技术面分析部分，该部分只通过使用技术分析方法分析股票交易数据并给出未来可能的走势。你应该尽可能保留原始分析结果，不要自己编造数据，在这节无需给出对应的交易策略。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在草稿中的参考文献部分列出。
    请以markdown格式输出，务必保持草稿中的其它部分内容不变。
    请返回撰写后的草稿全文。
    """
    draft3 = call_model(content = prompt3)
    with open("try/draft3.md", "w", encoding="utf-8") as file:
            file.write(draft3)

    memory_report = asyncio.run(memory(draft3))

    prompt4 =f"""你是一位金融分析报告写作者，你的唯一目标是根据提供的草稿和文章，撰写报告中的指定部分。
    文章: '{memory_report}'
    草稿: '{draft3}'
    任务：你现在正在攥写草稿中summary:结论与投资建议部分，该部分需要给出具体的投资建议，并给出相应的买入与卖出策略，格式为 1.xx股票 对应的分析结果；2.xx股票 对应的分析结果；3.xx股票 对应的分析结果...并按推荐度从高到低进行排序。你应该尽可能保留原始分析结果，不要自己编造数据。请你仅根据提供的文章内容结合草稿上下文撰写,请尽可能使用提供文章中的原文，撰写后部分字数不得低于原文的80%。如果你使用的原文内容或数据有参考文献，请在草稿中的参考文献部分列出。
    请以markdown格式输出，务必保持草稿中的其它部分内容不变。
    请返回撰写后的结论与投资建议部分。
    """
    draft4 = call_model(content = prompt4)
    with open("try/draft4.md", "w", encoding="utf-8") as file:
            file.write(draft4)

    draft = draft3.replace("summary:结论与投资建议","summary:结论与投资建议"+draft4)
    with open("try/writer_report.md", "w", encoding="utf-8") as file:
            file.write(draft)

    reviewer_report = call_model(content= "你是一名专业的金融分析报告审稿人。你被要求审阅一份由非专业人士撰写的初稿。如果初稿质量足够好，可以发布，请接受该初稿；否则，请提供适当的修订意见。关于个股的操作建议，务必结合历史数据进行,具体初稿如下："+draft)
    with open("try/reviewer_report.md", "w", encoding="utf-8") as file:
        file.write(reviewer_report)

    prom = f"""你是一位专业的金融分析报告编辑,你的目标是根据审阅者的意见对金融分析报告初稿进行修订。你被审阅者委以重任，负责修订一份由非专业人士撰写的初稿。如果你决定遵循审阅者的意见，请在初稿基础上进行修改，并确保解决他们提出的所有问题，并根据内容为每个章节重新拟制合适的标题。
    审阅者提供的意见：'{reviewer_report}'
    金融分析报告: '{draft}'
    要点：务必保证原报告的结构和完整性，字数不得低于原报告，除了审阅者提供意见的地方，报告其余部分保持不变，不要删去任何内容。
    请使用Markdown格式回答，但不要用任何代码块（如 ```）包裹内容。直接以Markdown语法输出。
    """
    revise_report = call_model(content= prom)

    with open("try/revise_report.md", "w", encoding="utf-8") as file:
        file.write(revise_report)
    t2 = time.time()
    print(t2-t1)



    