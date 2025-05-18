import sys

sys.path.append("./")

from db.service.knowledge_base_service import qa_release_valiate


if __name__ == "__main__":
    docs = [
        {
            "id": "30615",
            "question": "可持续发展报告的发布年份是哪一年？",
            "answer": "2024年.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30616",
            "question": "可持续发展报告的发布公司是哪家？",
            "answer": "美新科技股份有限公司.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30617",
            "question": "可持续发展报告中关于绿色生态·环境篇的内容有哪些？",
            "answer": "包括循环经济、环境合规管理、污染物排放、废弃物处理、能源利用、水资源利用、应对气候变化、生态系统和生物多样性保护等内容.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30618",
            "question": "和谐共融·社会篇中涉及哪些内容？",
            "answer": "包括创新驱动、产品和服务安全与质量、数据安全与客户隐私保护、供应链安全、员工、社会贡献及乡村振兴等内容.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30619",
            "question": "精业笃行·治理篇中涉及哪些内容？",
            "answer": "包括尽职调查、利益相关方沟通、反商业贿赂及反贪污、反不正当竞争等内容.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30620",
            "question": "可持续发展报告中关于美新科技的介绍在哪一页？",
            "answer": "在第3页.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30621",
            "question": "可持续发展报告中关于ESG治理的内容在哪几页？",
            "answer": "在第4页、第5页.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30622",
            "question": "本报告是由哪家公司发布的？",
            "answer": "本报告是由美新科技股份有限公司发布的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30623",
            "question": "本报告是关于什么内容的？",
            "answer": "本报告是关于美新科技股份有限公司的年度可持续发展报告.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30624",
            "question": "本报告回应了哪些方面的重点关注议题？",
            "answer": "本报告回应了各利益相关方的重点关注议题,包括经济、社会、环境和公司治理等方面.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30625",
            "question": "本报告的时间范围是什么？",
            "answer": "本报告的时间范围是2024年1月1日至12月31日.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30626",
            "question": "报告中所采用的信息与数据来自于哪里？",
            "answer": "报告中所采用的信息与数据来自于美新科技股份有限公司及下属板块企业.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30627",
            "question": "报告中如无特别说明，所有金额均以什么货币表示？",
            "answer": "报告中如无特别说明,所有金额均以人民币表示.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30628",
            "question": "本报告是依据什么准则与框架编制而成的？",
            "answer": "本报告是依据<深圳证券交易所上市公司自律监管指引第17号⸺可持续发展报告(试行)>编制而成的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30629",
            "question": "报告所使用的语言是什么？",
            "answer": "报告所使用的语言为简体中文.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30630",
            "question": "报告以什么形式发布？",
            "answer": "报告以电子文档形式发布.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30631",
            "question": "电子文档可以在哪里查阅获取？",
            "answer": "电子文档可在公司网站(www.newtechwood.cn)及巨潮资讯网(www.cninfo.com.cn)中查阅获取.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30632",
            "question": "如果对报告有任何建议，应该如何联系？",
            "answer": "如果对报告有任何建议,应按报告中提供的联系方式联系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30633",
            "question": "“美新科技股份有限公司”在报告中如何表示？",
            "answer": "美新科技股份有限公司\"在报告中将以\"美新科技\"、\"美新\"、\"公司\"、\"我们\"表示.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30634",
            "question": "本报告是美新科技股份有限公司发布的第几份年度可持续发展报告？",
            "answer": "本报告是美新科技股份有限公司发布的第1份年度可持续发展报告.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30635",
            "question": "报告中披露了哪些方面的责任信息？",
            "answer": "报告中披露了美新科技股份有限公司及下属板块企业在履行经济、社会、环境和公司治理等方面责任的信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30636",
            "question": "报告中部分信息的时间范围是否仅限于2024年？",
            "answer": "报告中部分信息的时间范围可能超出2024年1月1日至12月31日.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30637",
            "question": "报告中所采用的数据是否包括下属板块企业？",
            "answer": "是的,报告中所采用的数据包括美新科技股份有限公司及下属板块企业.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30638",
            "question": "报告中是否说明了所有金额的货币单位？",
            "answer": "报告中如无特别说明,所有金额均以人民币表示.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30639",
            "question": "报告中是否提到了可持续发展的理念？",
            "answer": "报告结合了公司可持续发展理念、实践、绩效.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30640",
            "question": "报告中是否提到了可持续发展的实践？",
            "answer": "报告结合了公司可持续发展理念、实践、绩效.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30641",
            "question": "报告中是否提到了可持续发展的绩效？",
            "answer": "报告结合了公司可持续发展理念、实践、绩效.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30642",
            "question": "报告中是否提到了可持续发展的系统性回应？",
            "answer": "报告系统性回应了各利益相关方的重点关注议题.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30643",
            "question": "报告中是否提到了可持续发展的具体议题？",
            "answer": "报告系统性回应了各利益相关方的重点关注议题,具体议题未详细列出.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30644",
            "question": "报告中是否提到了可持续发展的具体时间范围？",
            "answer": "报告的时间范围是2024年1月1日至12月31日.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30645",
            "question": "报告中是否提到了可持续发展的具体数据来源？",
            "answer": "报告中所采用的信息与数据来自于美新科技股份有限公司及下属板块企业.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30646",
            "question": "报告中是否提到了可持续发展的具体准则与框架？",
            "answer": "报告是依据<深圳证券交易所上市公司自律监管指引第17号⸺可持续发展报告(试行)>编制而成的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30647",
            "question": "美新科技的地址在哪里？",
            "answer": "美新科技的地址位于惠州市惠东县大岭街道十二托乌塘地段.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30648",
            "question": "美新科技的邮箱是什么？",
            "answer": "美新科技的邮箱是xmzou@meixin-wpc.com.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30649",
            "question": "美新科技的联系电话是多少？",
            "answer": "美新科技的联系电话是0752-6531633.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30650",
            "question": "美新科技的董事长是谁？",
            "answer": "美新科技的董事长是林东融.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30651",
            "question": "美新科技的产品主要由哪些材料制成？",
            "answer": "美新科技的产品主要由循环再利用的资源制成,如塑料薄膜、塑料瓶、木屑等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30652",
            "question": "美新科技在2024年的主要发展方向是什么？",
            "answer": "美新科技在2024年的主要发展方向是以绿色环保助力循环经济,以技术创新驱动发展动能,并以企业责任严守合规底线.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30653",
            "question": "美新科技的主要业务是什么？",
            "answer": "美新科技的主要业务是高性能塑木复合材料的研发、生产和销售,产品包括户外地板、墙板、组合地板等新型环保塑木型材,广泛应用于家庭院落阳台、公用建筑设施、园林景观建设等户外环境.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30654",
            "question": "美新科技成立于哪一年？",
            "answer": "美新科技成立于2004年.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30655",
            "question": "美新科技的产品有哪些技术特点？",
            "answer": "美新科技的产品具有抗划痕、抗静电、耐污渍、不易开裂、不易霉变等技术特点,同时具有原木质感,更耐候、更耐磨、更美观.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30656",
            "question": "美新科技在哪一年上市？股票代码是什么？",
            "answer": "美新科技于2024年在深圳证券交易所创业板上市,股票代码为301588.sz.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30657",
            "question": "美新科技的产品获得了哪些认证？",
            "answer": "美新科技的产品获得了中国绿色产品认证、fsc森林管理体系认证、中国绿色建材产品认证、scs翠鸟回收物质含量认证、儿童安全级产品认证、韩国生态标签认证、新加坡绿色标签认证、健康建材产品认证、epd环境产品声明、leed能源与环境设计领导力、well健康建筑标准、breeam英国建筑研究院环境评估方法、法国hqe高质量环境等认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30658",
            "question": "美新科技的董事会是如何组成的？",
            "answer": "\"美新科技的董事会通过正式、透明的程序选出",
            "document_uuid": "确保选拔过程公正、有效.",
            "release_status": ""
        },
        {
            "id": "董事会由5名董事组成",
            "question": "其中独立董事占3名",
            "answer": "确保决策的独立性和客观性.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "提名委员会主席由独立董事担任",
            "question": "进一步强化了其在董事会治理中的领导作用.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "30659",
            "question": "美新科技的ESG治理架构是如何运作的？",
            "answer": "\"美新科技建立了稳健的esg治理架构",
            "document_uuid": "确保有效规划、实施和监督可持续发展策略.",
            "release_status": ""
        },
        {
            "id": "公司设立了专门的esg团队",
            "question": "负责监督各部门及子公司的可持续发展策略规划与执行.",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "esg团队每周召开联席例会",
            "question": "由公司主要负责人或分管副总经理主持",
            "answer": "确保esg议题在决策层得到充分关注.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "此外",
            "question": "esg团队每年向董事会提交年度报告",
            "answer": "汇报es的最新进展与成果.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30660",
            "question": "提名委员会在选拔新任董事时的流程是什么？",
            "answer": "\"提名委员会首先研究公司对新任董事及高级管理人员的人才需求",
            "document_uuid": "明确选拔标准.",
            "release_status": ""
        },
        {
            "id": "然后",
            "question": "在公司内部及外部人才市场进行全面搜寻",
            "answer": "物色初步候选人.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "最后",
            "question": "召开提名委员会会议",
            "answer": "依据既定的资格标准对候选人进行详细审核.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30661",
            "question": "董事会在ESG方面的主要职责是什么？",
            "answer": "董事会负责制定并检视esg策略和目标,评估重大esg相关问题并确定优先排序,审批esg策略并向利益相关者通报绩效和目标.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30662",
            "question": "ESG团队的主要职责是什么？",
            "answer": "esg团队负责制定和部署整个组织的esg举措,实施有效的esg监测及评估流程,监督各部门和子公司esg策略的执行情况,通过识别及管理esg机遇和风险以支持董事会决策.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30663",
            "question": "部门管理层在ESG方面的主要职责是什么？",
            "answer": "部门管理层负责执行董事会与esg团队分派的esg相关重点任务,执行并监控esg策略和目标的实施绩效,建立健全的esg数据追踪机制,认识并管理esg机遇和风险.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30664",
            "question": "美新科技如何应对公司规模快速扩张带来的风险？",
            "answer": "\"美新科技建立了健全的法人治理结构",
            "document_uuid": "制定了适应公司现阶段发展的内部控制体系并持续加强风险管理",
            "release_status": "以应对内外部环境的不确定性和潜在风险."
        },
        {
            "id": "同时",
            "question": "公司结合灵活的市场策略和多元化市场拓展",
            "answer": "及时调整风险管理机制",
            "document_uuid": "旨在尽可能有效地降低市场带来的风险.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "30665",
            "question": "美新科技在风险管理方面采取了哪些具体措施？",
            "answer": "\"美新科技注重加强与合作伙伴及行业联盟的合作",
            "document_uuid": "进一步提升自身的市场适应能力和抗风险能力.",
            "release_status": ""
        },
        {
            "id": "公司通过持续的技术创新和产品升级",
            "question": "保持了产品的市场竞争力.",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "此外",
            "question": "公司积极拓展国际市场",
            "answer": "销售网络覆盖全球50多个国家和地区",
            "document_uuid": "进一步分散了市场风险.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "30666",
            "question": "美新科技对哪些议题进行了适用性评估？",
            "answer": "\"美新科技根据<深圳证券交易所上市公司自律监管指引第17号⸺可持续发展报告(试行)>",
            "document_uuid": "对指引所提及的21项议题进行了适用性议题评估.",
            "release_status": ""
        },
        {
            "id": "评估结果显示",
            "question": "\"科技伦理\"\"和\"\"平等对待中小企业\"\"议题对于集团、业务板块、下属子公司均不适用.",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "30667",
            "question": "美新科技的产品有何特点？",
            "answer": "美新科技专注于塑木复合材料的研发与生产,其产品不仅在性能上具有显著优势,还契合国家绿色低碳循环发展的战略要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30668",
            "question": "美新科技的塑木产品主要使用哪些原料？",
            "answer": "美新科技的塑木产品主要使用再生塑料和植物纤维作为原料,其中再生塑料包括聚丙烯(pp)和聚乙烯(pe)等,植物纤维包括木粉、稻壳、秸秆等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30669",
            "question": "美新科技2024年度使用了多少吨再生塑料？",
            "answer": "美新科技2024年度使用了13,000吨再生塑料.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30670",
            "question": "美新科技的塑木产品在生产过程中如何实现环保？",
            "answer": "美新科技在生产过程中注重减少能源消耗和污染物达标排放,降低自身碳足迹,同时使用再生塑料和植物纤维作为原料,实现资源的循环利用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30671",
            "question": "美新科技的塑木产品是否可以循环再利用？",
            "answer": "是的,美新科技的塑木产品可以实现100%循环再利用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30672",
            "question": "美新科技如何处理生产过程中产生的边角料和不合格品？",
            "answer": "美新科技设立了破碎车间,配备了先进的破碎设备和技术团队,负责将生产过程中产生的边角料、不合格品及报废材料等进行精细破碎处理,重新投入到生产线中作为新塑木产品的原料使用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30673",
            "question": "美新科技的塑木产品有哪些特点？",
            "answer": "美新科技的塑木产品具有环保、健康、安全的特点,同时兼具木质外观与塑料耐用性,是一种新型材料.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30674",
            "question": "美新科技的塑木产品如何减少对环境的影响？",
            "answer": "美新科技的塑木产品通过使用再生塑料和植物纤维,减少了塑料垃圾对环境的污染,同时减少了对原始森林的砍伐,促进了农业废弃物的资源化利用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30675",
            "question": "美新科技的塑木产品中再生材料的比例是多少？",
            "answer": "美新科技的产品中超过85%的成分由循环再利用的资源再制而成.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30676",
            "question": "美新科技的塑木产品是否符合环保、健康、安全的原则？",
            "answer": "是的,美新科技的塑木产品从原料到生产、销售及使用过程中均符合环保、健康、安全的原则.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30677",
            "question": "美新科技的塑木产品如何实现技术创新？",
            "answer": "美新科技通过技术创新实现产品及生产废弃物的循环转化,顺应了'绿色低碳循环'战略要求,助力可持续发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30678",
            "question": "美新科技在环境合规管理方面采取了哪些措施？",
            "answer": "\"美新科技将环境合规职责内化为企业运营的核心准则",
            "document_uuid": "建立了全方位、多层次的环境合规管理体系.",
            "release_status": ""
        },
        {
            "id": "公司严格遵守<中华人民共和国环境保护法>等法律法规",
            "question": "并制定了<环境因素识别及评价程序>等内部管理文件",
            "answer": "取得了iso 14001:2015环境管理体系认证.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "同时",
            "question": "公司还健全了环境突发事件应急管理体系",
            "answer": "着重提升应对突发事件的能力.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30679",
            "question": "美新科技如何确保环境保护工作的有效执行？",
            "answer": "\"美新科技以总经理为环境保护工作第一责任人",
            "document_uuid": "并设置环境保护与管理专职人员",
            "release_status": "负责统筹、落实并监督指导各项环境保护管理工作."
        },
        {
            "id": "各生产车间、班组负责落实日常环保工作",
            "question": "包括污染物处理设施运维、污染物例行监测、废弃物合规处置、资源能源节约利用等",
            "answer": "形成'三级'管理体系.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "公司还编制了<突发环境事件应急预案>",
            "question": "成立了环境应急管理小组",
            "answer": "并设置了应急池、消防设备等应急设施.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30680",
            "question": "美新科技在污染物排放管理上遵循什么原则？",
            "answer": "美新科技在污染物排放管理上遵循严守达标排放红线的原则,确保生产过程中产生的各类污染物均符合国家与地方环保标准.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30681",
            "question": "美新科技遵守哪些环境法律法规？",
            "answer": "美新科技严格遵守<中华人民共和国环境保护法><中华人民共和国水污染防治法><中华人民共和国大气污染防治法><中华人民共和国土壤污染防治法><中华人民共和国环境噪声污染防治法>等环境法律法规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30682",
            "question": "美新科技的哪些子公司没有设立生产基地？",
            "answer": "美新科技的中国香港子公司和美国子公司尚未设立生产基地.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30683",
            "question": "美新科技的哪些生产基地涉及废气排放？",
            "answer": "美新科技的惠州生产基地和建瓯工厂(在建)的工艺流程中主要涉及废气排放.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30684",
            "question": "美新科技的废气排放主要包含哪些污染物？",
            "answer": "美新科技的大气污染物主要包括非甲烷总烃(voc)和颗粒物.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30685",
            "question": "美新科技的废气排放来源是什么？",
            "answer": "美新科技的废气排放主要来源于成型共挤工艺及投料.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30686",
            "question": "美新科技如何确保污染防治设施有效运行？",
            "answer": "美新科技通过严格遵守环保法律法规,确保污染防治设施有效运行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30687",
            "question": "美新科技如何控制生产运营过程中的环境污染物？",
            "answer": "美新科技通过严格遵守环保法律法规,有效控制生产运营过程中产生的各类环境污染物.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30688",
            "question": "美新科技如何打造环境友好型企业？",
            "answer": "美新科技通过严格遵守环保法律法规,有效控制生产运营过程中产生的各类环境污染物,积极打造环境友好型企业.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30689",
            "question": "美新科技的经营活动是否符合当地环境保护法律法规的要求？",
            "answer": "美新科技的经营活动符合当地环境保护法律法规的要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30690",
            "question": "美新科技如何依法依规取得和更新排污许可证？",
            "answer": "美新科技已依法依规取得和更新排污许可证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30691",
            "question": "美新科技如何进行环境信息依法披露？",
            "answer": "美新科技按照规定进行环境信息依法披露.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30692",
            "question": "美新科技的子公司是否对环境有直接影响？",
            "answer": "美新科技的中国香港子公司和美国子公司尚未设立生产基地,无废水、废气排放及噪声影响.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30693",
            "question": "美新科技的惠州生产基地和建瓯工厂的废气排放对环境有何影响？",
            "answer": "美新科技的惠州生产基地和建瓯工厂的废气排放主要涉及非甲烷总烃(voc)和颗粒物,对环境有影响.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30694",
            "question": "美新科技的惠州生产基地和建瓯工厂的废水排放对环境有何影响？",
            "answer": "美新科技的惠州生产基地和建瓯工厂的生活污水对环境的直接影响较小.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30695",
            "question": "美新科技的惠州生产基地和建瓯工厂的噪声对环境有何影响？",
            "answer": "美新科技的惠州生产基地和建瓯工厂的噪声对环境的直接影响较小.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30696",
            "question": "美新科技的废气排放主要来源于哪些工艺？",
            "answer": "美新科技的废气排放主要来源于成型共挤工艺及投料.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30697",
            "question": "美新科技的废气排放中非甲烷总烃(VOC)和颗粒物分别来源于哪些工艺？",
            "answer": "美新科技的非甲烷总烃(voc)和颗粒物分别来源于成型共挤工艺及投料.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30698",
            "question": "公司如何处理VOC废气？",
            "answer": "公司采用集气罩收集voc废气,然后通过水喷淋和活性炭吸附处理,实现达标排放.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30699",
            "question": "公司如何处理颗粒物废气？",
            "answer": "公司采用管道收集颗粒物废气,然后通过布袋除尘处理,实现达标排放.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30700",
            "question": "公司对废气处理设施的运行情况如何管理？",
            "answer": "公司对废气处理设施的运行情况进行日常分级检查和记录,发现故障立即停止生产并报备抢修,确保其安全有效的运行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30701",
            "question": "公司委托第三方检测机构进行废气检测的频率是多少？",
            "answer": "公司委托第三方检测机构每年对公司有组织排放的废气进行两次检测,无组织排放的废气进行一次检测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30702",
            "question": "公司废气检测结果需要满足哪些标准？",
            "answer": "公司废气检测结果需要满足<大气污染综合排放标准>(gb 16297-1996)和<挥发性有机物无组织排放控制标准>(gb 37822-2019)中的相关要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30703",
            "question": "公司废气检测结果如何处理？",
            "answer": "公司按规定将检测结果上传至政府平台备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30704",
            "question": "公司废气处理设施的运行检查包括哪些内容？",
            "answer": "公司对废气处理设施的运行情况进行日常分级检查和记录,确保其安全有效的运行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30705",
            "question": "公司废气处理设施发生故障时如何处理？",
            "answer": "公司发现废气处理设施故障时,立即停止生产并报备抢修,确保其安全有效的运行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30706",
            "question": "公司废气处理设施的检测结果上传至何处？",
            "answer": "公司按规定将检测结果上传至政府平台备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30707",
            "question": "公司废气处理设施的检测结果是否需要满足特定标准？",
            "answer": "公司废气检测结果需要满足<大气污染综合排放标准>(gb 16297-1996)和<挥发性有机物无组织排放控制标准>(gb 37822-2019)中的相关要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30708",
            "question": "公司废气处理设施的检测结果上传至政府平台的目的是什么？",
            "answer": "公司按规定将检测结果上传至政府平台备案,以确保废气处理设施的运行符合相关标准.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30709",
            "question": "公司废气处理设施的检测结果上传至政府平台的时间是什么时候？",
            "answer": "公司按规定将检测结果上传至政府平台备案,具体时间未明确说明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30710",
            "question": "公司废气处理设施的检测结果上传至政府平台的频率是多少？",
            "answer": "公司按规定将检测结果上传至政府平台备案,具体频率未明确说明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30711",
            "question": "公司排污许可证和城镇污水排入排水管网许可证的作用是什么？",
            "answer": "保证合法性和有效性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30712",
            "question": "公司日常对污染物排放及污染防治设施运行情况进行监督检查的目的是什么？",
            "answer": "发现不符合项,要求责任部门进行整改,并跟踪监督.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30713",
            "question": "公司如何定期对污染物排放量进行管理？",
            "answer": "定期统计和监测污染物排放量,对年度检测结果进行留档记录.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30714",
            "question": "公司如何将污染物排放相关目标指标与各级责任人挂钩？",
            "answer": "将污染物排放相关目标指标与各级责任人职级评定、薪酬奖金挂钩.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30715",
            "question": "2024年，美新科技是否被纳入重点排污单位？",
            "answer": "未被纳入重点排污单位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30716",
            "question": "2024年，美新科技是否被列入环境信息依法强制披露单位企业名单？",
            "answer": "未被列入环境信息依法强制披露单位企业名单.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30717",
            "question": "2024年，美新科技是否因污染物排放合规问题接到当地社区居民投诉？",
            "answer": "未接到当地社区居民投诉.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30718",
            "question": "2024年，美新科技是否因污染物排放问题受到行政处罚或追究刑事责任？",
            "answer": "未受到行政处罚或追究刑事责任.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30719",
            "question": "2024年，美新科技是否接到社区和居民投诉？",
            "answer": "未接到社区和居民投诉.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30720",
            "question": "美新科技如何处理工业固体废弃物？",
            "answer": "坚持规范分类收集、分类贮存及委托运输、利用或处置各类工业固体废弃物.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30721",
            "question": "美新科技如何落实废弃物产生单位的主体责任？",
            "answer": "最大限度避免固体废弃物对环境产生负面影响.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30722",
            "question": "公司日常监督检查过程中发现不符合项后，会采取什么措施？",
            "answer": "要求责任部门进行整改,并对实施措施进行跟踪监督.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30723",
            "question": "公司对污染物排放量的统计和监测频率是怎样的？",
            "answer": "定期进行统计和监测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30724",
            "question": "公司对年度检测结果如何处理？",
            "answer": "进行留档记录.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30725",
            "question": "公司污染物排放相关目标指标与哪些方面挂钩？",
            "answer": "与各级责任人职级评定、薪酬奖金挂钩.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30726",
            "question": "2024年，美新科技是否因污染物排放问题被纳入重点监管？",
            "answer": "未被纳入重点排污单位,也未被列入环境信息依法强制披露单位企业名单.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30727",
            "question": "美新科技如何确保固体废弃物对环境的影响最小化？",
            "answer": "通过规范分类收集、分类贮存及委托运输、利用或处置各类工业固体废弃物来实现.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30728",
            "question": "美新科技遵守哪些法律法规？",
            "answer": "美新科技严格遵守<中华人民共和国固体废弃物污染环境防治法>、<危险废物管理计划和管理台账制定技术导则>(hj 1259-2022)、<危险废物贮存污染控制标准>(gb 18597-2023)等业务所在国家/地区的相关法律法规及标准指南.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30729",
            "question": "美新科技编制了哪些内部规章制度？",
            "answer": "美新科技编制了<危险废物处置管理规定>、<危险废物环境污染防治责任制>等内部规章制度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30730",
            "question": "美新科技对固体废物管理的原则是什么？",
            "answer": "美新科技以预防固体废物环境污染为主、以倡导固体废弃物综合利用为先,对固废废弃物产生至处置进行全面管理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30731",
            "question": "美新科技生产过程中产生的无害废弃物主要包括哪些？",
            "answer": "美新科技生产过程中产生的无害(一般固体)废弃物主要包括塑料包装物、废钢铁、木制品等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30732",
            "question": "美新科技如何管理无害废弃物？",
            "answer": "美新科技积极进行源头控制,设立专门的存放场地并标识清晰,要求相关人员按照规定类别进行存放,并通过系统平台记录管理台账.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30733",
            "question": "美新科技如何处理来料包装物？",
            "answer": "美新科技积极与供应商沟通,对部分来料包装物实施回收再利用计划,以减少资源浪费.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30734",
            "question": "对于具备回收价值的废弃物，美新科技如何处理？",
            "answer": "对于具备回收价值的废弃物,美新科技委托专业的第三方机构进行统一收集与处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30735",
            "question": "对于无法直接回收的废弃物，美新科技如何处理？",
            "answer": "对于无法直接回收的部分,在收集后则交由市政环卫部门处置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30736",
            "question": "美新科技生产过程中涉及哪些有害废弃物？",
            "answer": "美新科技生产过程中涉及废机油等有害废弃物.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30737",
            "question": "美新科技如何管理有害废弃物？",
            "answer": "美新科技对有害废弃物进行专门管理,确保其安全处置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30738",
            "question": "美新科技如何确保无害废弃物的存放安全？",
            "answer": "美新科技设立专门的存放场地并标识清晰,要求相关人员按照规定类别进行存放.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30739",
            "question": "美新科技如何减少资源浪费？",
            "answer": "美新科技积极与供应商沟通,对部分来料包装物实施回收再利用计划.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30740",
            "question": "美新科技如何处理无法直接回收的废弃物？",
            "answer": "美新科技将无法直接回收的废弃物收集后交由市政环卫部门处置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30741",
            "question": "美新科技如何确保废弃物的综合利用？",
            "answer": "美新科技积极与供应商沟通,对部分来料包装物实施回收再利用计划,并委托专业的第三方机构进行统一收集与处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30742",
            "question": "美新科技如何确保废弃物的合法处置？",
            "answer": "美新科技严格遵守相关法律法规及标准指南,编制内部规章制度,确保废弃物的合法处置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30743",
            "question": "美新科技如何确保废弃物管理的透明度？",
            "answer": "美新科技通过系统平台记录管理台账,确保废弃物管理的透明度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30744",
            "question": "美新科技如何确保废弃物管理的有效性？",
            "answer": "美新科技通过编制内部规章制度,设立专门的存放场地,委托专业的第三方机构进行统一收集与处理,确保废弃物管理的有效性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30745",
            "question": "美新科技如何确保废弃物管理的合规性？",
            "answer": "美新科技严格遵守相关法律法规及标准指南,编制内部规章制度,确保废弃物管理的合规性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30746",
            "question": "美新科技如何确保废弃物管理的可持续性？",
            "answer": "美新科技积极倡导固体废弃物综合利用,通过回收再利用计划,确保废弃物管理的可持续性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30747",
            "question": "美新科技如何确保废弃物管理的全面性？",
            "answer": "美新科技对固废废弃物产生至处置进行全面管理,确保废弃物管理的全面性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30748",
            "question": "美新科技如何确保废弃物管理的科学性？",
            "answer": "美新科技编制内部规章制度,设立专门的存放场地,通过系统平台记录管理台账,确保废弃物管理的科学性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30749",
            "question": "公司如何处理危险废弃物？",
            "answer": "公司将危险废物与一般固体废弃物、办公生活废弃物等按要求进行源头分类,设置危险废物警告标志牌和标签,合规暂存后,如实填写转移联单交由有资质的第三方进行收集处置,并进行管理台账记录.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30750",
            "question": "公司每年在广东省固体废物环境监管信息平台中做什么？",
            "answer": "公司按要求每年度在广东省固体废物环境监管信息平台中申报填写所产生、处置的固体废弃物情况,上传<危险废物管理计划>,并将危险废弃物过磅单、收运单、转移联单等进行备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30751",
            "question": "公司在建筑物设计阶段融入了哪些绿色节能理念？",
            "answer": "公司在建筑物设计阶段融入了绿色节能理念,推进建筑节能,全面考量了建筑物的自然采光、高效照明、保温隔热等核心需求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30752",
            "question": "美新科技的办公楼和实验楼获得了什么认证？",
            "answer": "美新科技新建的办公楼和实验楼成功通过了<绿色建筑评价标准>(22014版)一星级认定.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30753",
            "question": "公司内部制定了哪些能源管理制度？",
            "answer": "公司内部制定了<节能宣传培训制度><节能管理机构职责><节能奖惩管理制度><节水节电管理制度><能源采购控制程序>等相关能源管理制度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30754",
            "question": "公司采取了哪些措施优化照明系统？",
            "answer": "公司广泛采用了led节能灯具作为主要的照明光源,确保厂区及所有办公场所的照明功率密度均达到了现行规定值.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30755",
            "question": "公司惠州生产基地建立了什么体系？",
            "answer": "公司惠州生产基地按照国家标准<用能单位能源计量器具配备与管理通则>(gb17167-2006)的要求,建立了三级能源计量体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30756",
            "question": "公司如何确保能源消耗数据的准确性和可靠性？",
            "answer": "公司通过实时监测和数据分析,确保每一环节都配备了高精度的计量器具,从而精确掌握能源消耗的动态变化,及时发现能效运行的异常情况.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30757",
            "question": "公司采取了哪些措施提高能源利用效率？",
            "answer": "公司通过不断升级和更新节能技术提高能源利用效率,持续加快清洁能源替代,并取得了iso 50001:2018能源管理体系认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30758",
            "question": "公司如何确保照明系统的高效和节能？",
            "answer": "公司广泛采用了led节能灯具作为主要的照明光源,确保照明功率密度达到了现行规定值,积极构建绿色、低碳的生产和生活环境.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30759",
            "question": "公司如何管理能源使用情况？",
            "answer": "公司对能源使用情况进行严格监控和控制,通过不断升级和更新节能技术提高能源利用效率,并持续加快清洁能源替代.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30760",
            "question": "公司如何确保能源使用的规范性？",
            "answer": "公司通过内部制定的<节能宣传培训制度><节能管理机构职责><节能奖惩管理制度><节水节电管理制度><能源采购控制程序>等相关能源管理制度,持续加强对能源使用的规范.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30761",
            "question": "公司如何推进能源管理的规范化与高效化？",
            "answer": "公司取得了iso 50001:2018能源管理体系认证,并在生产运营中不断推进能源管理的规范化与高效化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30762",
            "question": "公司如何确保照明系统的标准符合性？",
            "answer": "公司严格遵循国家相关标准,确保厂区及所有办公场所的照明功率密度均达到了现行规定值.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30763",
            "question": "公司如何确保能源计量的准确性？",
            "answer": "公司惠州生产基地建立了三级能源计量体系,确保每一环节都配备了高精度的计量器具,从而确保数据的准确性和可靠性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30764",
            "question": "美新科技近年来在清洁能源转型方面采取了哪些措施？",
            "answer": "\"美新科技近年来加速清洁能源转型",
            "document_uuid": "于2023年布局屋顶光伏发电项目",
            "release_status": "装机容量达"
        },
        {
            "id": "3.5兆瓦",
            "question": "年发电量约占厂区总用电量的5%.",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "2024年",
            "question": "公司车间照明与停车场路灯全面升级为太阳能灯具",
            "answer": "并逐步以电动叉车取代柴油叉车",
            "document_uuid": "进一步加大了对可再生能源的利用力度.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "30765",
            "question": "美新科技的惠州生产基地光伏发电系统在2024年的发电量是多少？",
            "answer": "美新科技的惠州生产基地光伏发电系统在2024年的发电量为3,760,956千瓦时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30766",
            "question": "美新科技的光伏发电系统占厂区总用电量的比例是多少？",
            "answer": "美新科技的光伏发电系统年发电量约占厂区总用电量的5%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30767",
            "question": "美新科技在2024年采取了哪些措施来减少对电网的依赖？",
            "answer": "美新科技在2024年采取了车间照明与停车场路灯全面升级为太阳能灯具,以及逐步以电动叉车取代柴油叉车的措施来减少对电网的依赖.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30768",
            "question": "美新科技的光伏发电系统装机容量是多少？",
            "answer": "\"美新科技的光伏发电系统装机容量为",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "3.5兆瓦.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30769",
            "question": "美新科技的光伏发电系统在2024年的发电量占总用电量的比例是多少？",
            "answer": "美新科技的光伏发电系统在2024年的发电量占总用电量的比例约为5%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30770",
            "question": "美新科技的光伏发电系统在2024年发电量的具体数值是多少？",
            "answer": "美新科技的光伏发电系统在2024年发电量的具体数值为3,760,956千瓦时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30771",
            "question": "美新科技在2024年采取了哪些措施来提升清洁能源在企业能源结构中的占比？",
            "answer": "美新科技在2024年采取了车间照明与停车场路灯全面升级为太阳能灯具,以及逐步以电动叉车取代柴油叉车的措施来提升清洁能源在企业能源结构中的占比.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30772",
            "question": "美新科技的光伏发电系统在2024年发电量的具体数值是多少千瓦时？",
            "answer": "美新科技的光伏发电系统在2024年发电量的具体数值为3,760,956千瓦时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30773",
            "question": "公司建立的集装箱式储能电站的储能容量是多少？",
            "answer": "公司建立的集装箱式储能电站的储能容量为9mw/20.1mwh.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30774",
            "question": "公司如何利用储能电站实现电力削峰填谷？",
            "answer": "公司通过储能电站在电价低谷时段智能地储存电能,在电力需求高峰时段释放存储的电能,实现了电力的削峰填谷.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30775",
            "question": "2024年公司光伏发电系统的发电量是多少？",
            "answer": "2024年公司光伏发电系统的发电量为3,760,956电力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30776",
            "question": "公司被纳入广东省重点用能单位后需要做什么？",
            "answer": "公司被纳入广东省重点用能单位后,需要按规定编制<能源利用状况报告>,并及时完成系统填报,同时接受有资质第三方的外部审计.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30777",
            "question": "公司每月对能源使用数据进行哪些操作？",
            "answer": "公司每月对能源使用数据进行统计、上报、存档及分析总结.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30778",
            "question": "公司如何通过能源管理降低制造成本？",
            "answer": "公司通过峰谷价差套利机制,利用储能电站在电价低谷时段储存电能,在高峰时段释放电能,从而降低制造成本.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30779",
            "question": "公司储能电站的核心储能单元是什么？",
            "answer": "公司储能电站的核心储能单元是高性能的电池组.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30780",
            "question": "公司如何跟踪年度能源管理与目标进展？",
            "answer": "公司通过每月统计、上报、存档及分析总结能源使用数据,由知产法务部每年开展内部能源审计工作并纳入相关责任部门、人员年度绩效考核,来跟踪年度能源管理与目标进展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30781",
            "question": "公司储能电站的创新布局带来了哪些好处？",
            "answer": "公司储能电站的创新布局优化了电网的负载平衡,实现了电力削峰填谷,并通过峰谷价差套利机制降低了制造成本.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30782",
            "question": "公司2024年的能耗强度是多少？",
            "answer": "公司2024年的能耗强度为0.1吨标煤/万元营收.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30783",
            "question": "美新科技采取了哪些主要节水措施？",
            "answer": "\"美新科技采取了芯棒水回用系统",
            "document_uuid": "将市政水替换为循环水",
            "release_status": "每天节约超过150吨市政用水"
        },
        {
            "id": "此外",
            "question": "公司还对车间管道进行了全面改造",
            "answer": "增设了中水处理设备",
            "document_uuid": "预计全年最低可节省用水达50",
            "release_status": "400吨.\"",
            "": "qa_await"
        },
        {
            "id": "30784",
            "question": "美新科技的水资源重复利用率是多少？",
            "answer": "美新科技的水资源重复利用率高达95%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30785",
            "question": "2024年美新科技的总耗水量是多少？",
            "answer": "2024年美新科技的总耗水量为173,119吨.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30786",
            "question": "美新科技如何利用雨水？",
            "answer": "美新科技设立了高效的雨水收集系统,充分利用自然降水进行清洁、灌溉等,有效地减少水资源消耗、提升节水效果.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30787",
            "question": "美新科技2024年的总用水强度是多少？",
            "answer": "\"美新科技2024年的总用水强度为",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "2.07吨/万元营收.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30788",
            "question": "美新科技如何应对气候变化？",
            "answer": "\"美新科技积极应对气候变化",
            "document_uuid": "响应联合国可持续发展目标",
            "release_status": "遵循<联合国气候变化框架公约><巴黎协定>等相关国际公约"
        },
        {
            "id": "公司严格遵守相关法律法规",
            "question": "选择合适的项目选址",
            "answer": "避免在重要生态功能区或生态环境敏感脆弱区建设或运营生产经营活动.",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "同时",
            "question": "公司致力于降低碳排放",
            "answer": "优化生产流程",
            "document_uuid": "推动技术创新",
            "release_status": "全方位投身于应对气候变化的行动.\"",
            "": "qa_await"
        },
        {
            "id": "30789",
            "question": "美新科技的企业社会责任体现在哪些方面？",
            "answer": "美新科技支持乡村振兴和公益事业,以实际行动践行企业社会责任,持续回馈社会.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30790",
            "question": "美新科技的产品理念是什么？",
            "answer": "美新科技秉持追求卓越的产品理念,充分发扬产品绿色属性,以市场需求为导向,不断推出具有创新性、前瞻性和可持续性的产品.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30791",
            "question": "美新科技的核心战略定位是什么？",
            "answer": "美新科技将创新驱动作为实现公司\"国际化、品牌化\"战略定位的核心动力和关键力量.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30792",
            "question": "美新科技在技术研发方面有哪些措施？",
            "answer": "美新科技持续加大产品研发力度,全面优化产品生产工艺及流程,加速推进自动化及数智化转型,积极开拓市场和商业模式.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30793",
            "question": "美新科技的核心领域是什么？",
            "answer": "美新科技立足于新型环保塑木型材核心领域.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30794",
            "question": "美新科技如何推进创新研发？",
            "answer": "美新科技通过立项审批,进行技术可行性分析、市场前景评估和资源投入规划,来推进创新研发.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30795",
            "question": "美新科技的产品对行业发展有何影响？",
            "answer": "美新科技的产品赋能行业发展,以新一代塑木复合材料前沿技术引领行业迈向新阶段.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30796",
            "question": "美新科技如何支持乡村振兴？",
            "answer": "美新科技支持乡村振兴,以实际行动践行企业社会责任,持续回馈社会.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30797",
            "question": "美新科技的创新研发全生命周期管理包括哪些步骤？",
            "answer": "美新科技的创新研发全生命周期管理包括立项审批,进行技术可行性分析、市场前景评估和资源投入规划.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30798",
            "question": "美新科技如何优化产品生产工艺及流程？",
            "answer": "美新科技通过全面优化产品生产工艺及流程,加速推进自动化及数智化转型来优化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30799",
            "question": "美新科技如何开拓市场和商业模式？",
            "answer": "美新科技积极开拓市场和商业模式,以新一代塑木复合材料前沿技术引领行业.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30800",
            "question": "美新科技的创新研发全生命周期管理的目的是什么？",
            "answer": "美新科技的创新研发全生命周期管理的目的是确保研发项目的可行性、市场前景和资源投入规划,以实现创新目标.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30801",
            "question": "美新科技如何实现自动化及数智化转型？",
            "answer": "美新科技通过加速推进自动化及数智化转型来实现这一目标.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30802",
            "question": "美新科技如何进行市场前景评估？",
            "answer": "美新科技在立项审批阶段进行市场前景评估,以确保项目的市场适应性和成功可能性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30803",
            "question": "美新科技如何进行资源投入规划？",
            "answer": "美新科技在立项审批阶段进行资源投入规划,以确保项目的资源合理分配和有效利用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30804",
            "question": "美新科技如何进行技术可行性分析？",
            "answer": "美新科技在立项审批阶段进行技术可行性分析,以确保项目的实施可能性和技术基础.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30805",
            "question": "过程控制的主要目标是什么？",
            "answer": "过程控制的主要目标是实施严格的规范控制,确保项目按照既定的时间表和质量标准推进.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30806",
            "question": "美新科技的创新研发团队由哪些部门组成？",
            "answer": "美新科技的创新研发团队由技术部、产品开发部和设备模具开发部组成.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30807",
            "question": "技术部的主要职责是什么？",
            "answer": "技术部主要负责原材料及配方的研发、改进和升级,通过对原材料的深入研究和技术优化,提升产品的整体质量和性能.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30808",
            "question": "产品开发部的主要职责是什么？",
            "answer": "产品开发部主要负责产品及其外观的设计与研发,通过不断推出符合市场需求的新产品,帮助公司在激烈的市场竞争中保持领先地位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30809",
            "question": "设备模具开发部的主要职责是什么？",
            "answer": "设备模具开发部专注于配套设备及模具的开发.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30810",
            "question": "本报告包含哪些内容？",
            "answer": "\"本报告包含董事长致辞、关于美新科技、可持续发展方针、绿色生态",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "环境篇、和谐共融",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "社会篇、精业笃行",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "治理篇和附录等内容.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30811",
            "question": "美新科技的核心业务是什么？",
            "answer": "美新科技的核心业务围绕创新研发团队展开,包括技术部、产品开发部和设备模具开发部的工作.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30812",
            "question": "技术部如何提升产品的整体质量和性能？",
            "answer": "技术部通过深入研究原材料和技术优化,研发、改进和升级原材料及配方,从而提升产品的整体质量和性能.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30813",
            "question": "产品开发部如何帮助公司在市场竞争中保持领先地位？",
            "answer": "产品开发部通过不断推出符合市场需求的新产品,帮助公司在激烈的市场竞争中保持领先地位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30814",
            "question": "设备模具开发部的工作重点是什么？",
            "answer": "设备模具开发部的工作重点是配套设备及模具的开发.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30815",
            "question": "过程控制需要遵循哪些标准？",
            "answer": "过程控制需要遵循既定的时间表和质量标准.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30816",
            "question": "美新科技的可持续发展方针包含哪些方面？",
            "answer": "\"美新科技的可持续发展方针包含绿色生态",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "环境篇、和谐共融",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "社会篇和精业笃行",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "治理篇.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30817",
            "question": "本报告的附录部分可能包含哪些内容？",
            "answer": "本报告的附录部分可能包含与报告内容相关的补充资料或详细数据.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30818",
            "question": "美新科技的创新研发团队有多少人？",
            "answer": "美新科技的创新研发团队总人数达到94人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30819",
            "question": "美新科技如何快速响应市场变化？",
            "answer": "通过各部门的紧密合作,美新科技能够快速响应市场变化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30820",
            "question": "美新科技如何持续推出具有竞争力的创新产品？",
            "answer": "通过各部门的紧密合作,美新科技能够持续推出具有竞争力的创新产品.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30821",
            "question": "美新科技如何巩固其在行业中的领先地位？",
            "answer": "通过持续推出具有竞争力的创新产品,美新科技巩固了其在行业中的领先地位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30822",
            "question": "美新科技建立了哪些研发平台？",
            "answer": "美新科技建立了'研发打卡工时平台'和'研发领料平台'.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30823",
            "question": "研发打卡工时平台的主要功能是什么？",
            "answer": "研发打卡工时平台主要用于记录研发人员的工时投入,实时跟踪项目进展,优化资源配置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30824",
            "question": "研发领料平台的主要功能是什么？",
            "answer": "研发领料平台主要用于记录研发过程中所需的原材料、设备及其他物资的领用情况,实现物料管理和成本透明化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30825",
            "question": "双平台的协同作用是什么？",
            "answer": "双平台的协同作用通过对工时数据和领料数据的整合与分析,全面掌握每个项目的资源投入,确保项目全流程管控,并明确了项目后期的汇报流程和结项标准.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30826",
            "question": "美新科技如何推动创新战略落地和成果转化？",
            "answer": "美新科技通过全面开展科技创新实践,积极推动创新战略落地和成果转化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30827",
            "question": "美新科技如何实现人才与发展的双向适配？",
            "answer": "美新科技通过产学研合作、人才培育、人才激励等方面实现人才与发展的双向适配.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30828",
            "question": "美新科技如何营造良好的创新文化氛围？",
            "answer": "美新科技通过产学研合作、人才培育、人才激励等方面营造良好的创新文化氛围.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30829",
            "question": "美新科技如何建立知识产权全流程规范管理？",
            "answer": "美新科技建立了知识产权全流程规范管理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30830",
            "question": "美新科技如何设计和制造设备模具？",
            "answer": "美新科技通过设计和制造高效、精准的设备模具,为生产流程提供了强有力的技术支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30831",
            "question": "美新科技如何为生产流程提供技术支持？",
            "answer": "美新科技通过设计和制造高效、精准的设备模具,为生产流程提供了强有力的技术支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30832",
            "question": "美新科技如何进行精细化管理？",
            "answer": "美新科技通过内部创新建立'研发打卡工时平台'和'研发领料平台',对研发创新项目进行精细化管理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30833",
            "question": "美新科技如何优化资源配置？",
            "answer": "美新科技通过研发打卡工时平台优化资源配置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30834",
            "question": "美新科技如何实现物料管理和成本透明化？",
            "answer": "美新科技通过研发领料平台实现物料管理和成本透明化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30835",
            "question": "美新科技如何确保项目全流程管控？",
            "answer": "美新科技通过双平台的协同作用确保项目全流程管控.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30836",
            "question": "美新科技如何明确项目后期的汇报流程和结项标准？",
            "answer": "美新科技通过双平台的协同作用明确了项目后期的汇报流程和结项标准.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30837",
            "question": "美新科技在2024年进行了哪些研发项目？",
            "answer": "美新科技在2024年进行了多项研发项目,包括自动化原木四面切削与码垛技术等,覆盖了从原材料优化到生产工艺升级等领域.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30838",
            "question": "美新科技如何强化内部创新？",
            "answer": "美新科技通过不断探索新技术、新配方、新产品和新工艺,以及开展多项研发周期较短的中小型研发创新项目,来强化内部创新.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30839",
            "question": "美新科技在2024年与哪些外部机构开展了研发合作？",
            "answer": "美新科技在2024年先后与香港理工大学、纳米及先进材料研发院有限公司、香港生产力促进局等开展了研发合作.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30840",
            "question": "美新科技与上游供应商的合作内容是什么？",
            "answer": "美新科技与上游供应商紧密协作,针对产品原材料配方和生产机械研发进行深入交流与联合攻关,以提升产品性能和生产效率.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30841",
            "question": "美新科技的创新模式如何促进技术进步？",
            "answer": "美新科技通过开放协同的创新模式,不仅增强了公司的技术竞争力,也为行业的技术进步和可持续发展注入了新的活力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30842",
            "question": "美新科技的研发项目覆盖了哪些领域？",
            "answer": "美新科技的研发项目覆盖了从原材料优化到生产工艺升级等多个领域.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30843",
            "question": "美新科技如何实现内外部双轮驱动？",
            "answer": "美新科技通过积极联合外部机构、产业链上下游及高校,开展全方位的技术交流与研发合作,实现了内外部双轮驱动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30844",
            "question": "美新科技的创新成果如何保障？",
            "answer": "美新科技通过高效推进创新研发项目,不断探索新技术、新配方、新产品和新工艺,以保持在行业中的技术领先地位,从而充分保障创新成果权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30845",
            "question": "美新科技的创新模式有哪些特点？",
            "answer": "美新科技的创新模式特点是开放协同,不仅增强了公司的技术竞争力,也为行业的技术进步和可持续发展注入了新的活力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30846",
            "question": "美新科技如何加速创新成果转化？",
            "answer": "美新科技通过与外部机构在专业领域的技术优势合作,加速了创新成果转化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30847",
            "question": "美新科技的研发合作对象有哪些？",
            "answer": "美新科技的研发合作对象包括香港理工大学、纳米及先进材料研发院有限公司、香港生产力促进局等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30848",
            "question": "美新科技的研发合作如何提升产品性能？",
            "answer": "美新科技通过与上游供应商紧密协作,针对产品原材料配方和生产机械研发进行深入交流与联合攻关,从而提升了产品性能.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30849",
            "question": "美新科技的研发合作如何提高生产效率？",
            "answer": "美新科技通过与上游供应商紧密协作,针对生产机械研发进行深入交流与联合攻关,从而提高了生产效率.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30850",
            "question": "美新科技的研发合作如何促进技术突破？",
            "answer": "美新科技通过与外部机构在专业领域的技术优势合作,促进了技术突破.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30851",
            "question": "美新科技的研发合作如何推动产业升级？",
            "answer": "美新科技通过与外部机构在专业领域的技术优势合作,推动了产业升级.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30852",
            "question": "美新科技的研发合作如何增强公司的技术竞争力？",
            "answer": "美新科技通过与外部机构在专业领域的技术优势合作,增强了公司的技术竞争力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30853",
            "question": "美新科技的研发合作如何促进行业的可持续发展？",
            "answer": "美新科技通过与外部机构在专业领域的技术优势合作,为行业的可持续发展注入了新的活力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30854",
            "question": "美新科技如何保障公司的竞争优势及创新能力？",
            "answer": "美新科技严格遵守<中华人民共和国专利法><中华人民共和国商标法>等国内外知识产权相关法律法规,结合自身研发特点,制定<知识产权控制程序>等制度文件,全面覆盖产品及技术开发流程的知识产权管理,确保对创新成果及时进行评估和知识产权保护.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30855",
            "question": "2024年，美新科技修订了哪些知识产权控制程序？",
            "answer": "2024年,美新科技对<知识产权获取控制程序><知识产权维护控制程序><知识产权运用控制程序><知识产权风险管理控制程序><知识产权争议处理控制程序>和<知识产权类合同控制程序>等6项知识产权控制程序及1项保密控制程序进行修订.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30856",
            "question": "美新科技设立的知产法务部主要负责什么工作？",
            "answer": "美新科技设立的知产法务部主要负责定期进行知识产权的检索和监控,精准把握行业发展动态.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30857",
            "question": "美新科技的知识产权管理体系包括哪些方面？",
            "answer": "美新科技的知识产权管理体系包括知识产权获取、维护、运用、风险管理、争议处理和知识产权类合同控制等方面.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30858",
            "question": "美新科技为什么要修订知识产权控制程序？",
            "answer": "美新科技修订知识产权控制程序是为了进一步完善知识产权管理体系,确保公司的竞争优势及创新能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30859",
            "question": "美新科技的知识产权控制程序有哪些？",
            "answer": "美新科技的知识产权控制程序包括<知识产权获取控制程序><知识产权维护控制程序><知识产权运用控制程序><知识产权风险管理控制程序><知识产权争议处理控制程序>和<知识产权类合同控制程序>.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30860",
            "question": "美新科技如何确保创新成果得到及时的知识产权保护？",
            "answer": "美新科技通过制定<知识产权控制程序>等制度文件,全面覆盖产品及技术开发流程的知识产权管理,确保对创新成果及时进行评估和知识产权保护.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30861",
            "question": "美新科技的知识产权管理体系是否覆盖了产品及技术开发流程？",
            "answer": "是的,美新科技的知识产权管理体系全面覆盖了产品及技术开发流程.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30862",
            "question": "美新科技的知识产权控制程序修订了多少项？",
            "answer": "美新科技在2024年修订了6项知识产权控制程序及1项保密控制程序.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30863",
            "question": "美新科技的知识产权控制程序修订的目的是什么？",
            "answer": "美新科技的知识产权控制程序修订的目的是进一步完善知识产权管理体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30864",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的竞争优势？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的竞争优势.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30865",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的创新能力？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的创新能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30866",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的知识产权管理水平？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的知识产权管理水平.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30867",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的知识产权保护能力？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的知识产权保护能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30868",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的知识产权运用效率？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的知识产权运用效率.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30869",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的知识产权风险管理能力？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的知识产权风险管理能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30870",
            "question": "美新科技的知识产权控制程序修订后，是否有助于提升公司的知识产权争议处理能力？",
            "answer": "是的,美新科技的知识产权控制程序修订后,有助于提升公司的知识产权争议处理能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30871",
            "question": "美新科技如何应对知识产权侵权行为？",
            "answer": "一旦发现知识产权侵权事件,美新科技将通过聘请专业法律团队并采取有效的行动来应对.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30872",
            "question": "美新科技在保密协议中设置了哪些条款？",
            "answer": "美新科技在保密协议中设置了知识产权保护的相关条款,要求与供应商和利益相关方合作时签署并严格遵守相关要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30873",
            "question": "2024年美新科技开展了哪些培训？",
            "answer": "2024年,美新科技开展了iso内审员培训,涵盖有关知识产权的相关内容,共计参与人数25人,培训总时长100小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30874",
            "question": "美新科技获得了哪些认证？",
            "answer": "截至报告期,美新科技已获得gb/t29490:2013-知识产权管理体系认证证书.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30875",
            "question": "美新科技如何提升员工对知识产权保护的意识？",
            "answer": "美新科技通过开展iso内审员培训,涵盖有关知识产权的相关内容,进一步提升员工对知识产权保护的意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30876",
            "question": "美新科技的培训参与人数是多少？",
            "answer": "美新科技的培训参与人数共计25人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30877",
            "question": "美新科技的培训总时长是多少？",
            "answer": "美新科技的培训总时长为110小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30878",
            "question": "美新科技的创新战略与企业发展战略如何融合？",
            "answer": "美新科技通过进一步明确创新方向,凝聚创新共识,将创新战略与企业发展战略充分融合.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30879",
            "question": "美新科技如何确保与供应商和利益相关方合作中的知识产权保护？",
            "answer": "美新科技在保密协议中设置了知识产权保护的相关条款,并要求签署并严格遵守相关要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30880",
            "question": "美新科技的ISO内审员培训内容包括哪些？",
            "answer": "美新科技的iso内审员培训内容包括有关知识产权的相关内容.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30881",
            "question": "美新科技的培训目的是什么？",
            "answer": "美新科技的培训目的是进一步提升员工对知识产权保护的意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30882",
            "question": "美新科技的培训对象是谁？",
            "answer": "美新科技的培训对象是公司员工.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30883",
            "question": "美新科技的培训时间是多久？",
            "answer": "美新科技的培训总时长为100小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30884",
            "question": "美新科技的培训内容是否包括知识产权保护？",
            "answer": "美新科技的培训内容包括有关知识产权保护的相关内容.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30885",
            "question": "美新科技的短期科技创新目标是什么？",
            "answer": "美新科技的短期科技创新目标是在关键产品中引入新技术,提升产品性能与用户体验,降低生产成本.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30886",
            "question": "中期科技创新目标包括哪些内容？",
            "answer": "中期科技创新目标包括推出多款具有行业领先技术的新产品,拓展新市场领域,实现年度营业收入稳定增长.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30887",
            "question": "长期科技创新目标是什么？",
            "answer": "长期科技创新目标是成为行业技术创新引领者,建立完善的技术创新体系,在前沿技术领域取得多项重大突破.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30888",
            "question": "美新科技在2024年做了哪些创新尝试？",
            "answer": "美新科技在2024年已在关键产品中逐步引入创新技术,提升各类性能属性,包括防火等级、防滑等级及防静电等级等,以满足多样化的客户需求和拓宽不同的应用场景.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30889",
            "question": "美新科技开发了哪些新产品？",
            "answer": "美新科技已逐步开发与塑木产品相关的其他新产品,如葡萄架、凉亭、户外家具等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30890",
            "question": "短期目标的创新重点是什么？",
            "answer": "短期目标的创新重点是优化核心产品.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30891",
            "question": "中期目标的创新重点是什么？",
            "answer": "中期目标的创新重点是开拓产品类型.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30892",
            "question": "长期目标的创新重点是什么？",
            "answer": "长期目标的创新重点是完善创新体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30893",
            "question": "美新科技如何激发员工的创新动力？",
            "answer": "美新科技通过设立从短期、中期到长期的科技创新目标,更好地衡量和评估创新战略的落地和实施情况,从而激发员工的创新动力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30894",
            "question": "美新科技的创新内容有哪些？",
            "answer": "\"美新科技的创新内容包括在关键产品中引入新技术",
            "document_uuid": "提升产品性能与用户体验",
            "release_status": "降低生产成本"
        },
        {
            "id": "推出多款具有行业领先技术的新产品",
            "question": "拓展新市场领域",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "成为行业技术创新引领者",
            "question": "建立完善的技术创新体系",
            "answer": "在前沿技术领域取得多项重大突破.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30895",
            "question": "美新科技的创新目标如何帮助公司发展？",
            "answer": "美新科技的创新目标通过优化核心产品、开拓产品类型和完善创新体系,帮助公司提升产品性能,拓展市场,实现营业收入增长,最终成为行业技术创新的引领者.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30896",
            "question": "美新科技的创新目标如何满足客户需求？",
            "answer": "美新科技通过引入新技术提升产品性能,如防火等级、防滑等级及防静电等级等,满足多样化的客户需求,并通过开发新产品如葡萄架、凉亭、户外家具等,拓宽不同的应用场景.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30897",
            "question": "美新科技2024年的研发创新相关总投入金额是多少？",
            "answer": "2024年美新科技的研发创新相关总投入金额为24,431,908.94元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30898",
            "question": "研发创新相关投入占销售收入的比例是多少？",
            "answer": "\"研发创新相关投入占销售收入的比例为",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "2.93%.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30899",
            "question": "美新科技的研发人员总人数是多少？",
            "answer": "美新科技的研发人员总人数为94人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30900",
            "question": "研发人员占公司总人数的比例是多少？",
            "answer": "研发人员占公司总人数的比例为10.39%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30901",
            "question": "美新科技新增专利申请总数是多少？",
            "answer": "美新科技新增专利申请总数为35项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30902",
            "question": "美新科技新增专利授权总数是多少？",
            "answer": "美新科技新增专利授权总数为22项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30903",
            "question": "美新科技累计有效专利总数是多少？",
            "answer": "美新科技累计有效专利总数为202项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30904",
            "question": "美新科技的发明专利数量是多少？",
            "answer": "美新科技的发明专利数量为11项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30905",
            "question": "美新科技的外观设计专利数量是多少？",
            "answer": "美新科技的外观设计专利数量为155项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30906",
            "question": "美新科技的实用新型专利数量是多少？",
            "answer": "美新科技的实用新型专利数量为36项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30907",
            "question": "美新科技新增编制标准数量是多少？",
            "answer": "美新科技新增编制标准数量为10项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30908",
            "question": "美新科技累计编制标准数量是多少？",
            "answer": "美新科技累计编制标准数量为27项.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30909",
            "question": "美新科技参与的行业协会数量是多少？",
            "answer": "美新科技参与的行业协会数量为2个.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30910",
            "question": "美新科技获得的广东省塑木复合材料工程技术研究开发中心是由哪些机构颁发的？",
            "answer": "广东省塑木复合材料工程技术研究开发中心由广东省科学技术厅、广东省发展和改革委员会、广东省经济和信息化委员会颁发.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30911",
            "question": "美新科技获得的高新技术企业证书是由哪些机构颁发的？",
            "answer": "高新技术企业证书由广东省科学技术厅、广东省财政厅、广东省国家税务局、广东省地方税务局颁发.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30912",
            "question": "美新科技的产品和服务的重要性体现在哪里？",
            "answer": "\"产品和服务是企业安身立命之根本",
            "document_uuid": "也是决定企业发展的关键因素.",
            "release_status": ""
        },
        {
            "id": "美新科技始终坚持以最优的产品和服务为公司客户提供最大的价值.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30913",
            "question": "美新科技如何确保产品质量和服务符合要求？",
            "answer": "美新科技严格遵守<中华人民共和国产品质量法>等相关法律法规,通过制定<产品含量限制控制程序><原材料来料检验标准>等管理程序及质量检验标准,对生产和服务提供过程进行有效控制.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30914",
            "question": "美新科技是否通过了ISO 9001质量管理体系认证？",
            "answer": "是的,报告期内,公司已通过iso 9001质量管理体系认证,确保内部质量管理体系持续有效运行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30915",
            "question": "美新科技制定了哪些质量控制文件？",
            "answer": "美新科技结合产品标准及法规要求制定了科学的产品质量控制文件,包括<产品含量限制控制程序><原材料来料检验标准>等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30916",
            "question": "美新科技的质量控制流程是什么？",
            "answer": "美新科技实施了全面且严格的质量控制流程,全面落实质量保障相关工作,确保产品质量和服务符合要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30917",
            "question": "美新科技的质量管理体系认证证书在哪里可以查看？",
            "answer": "美新科技的质量管理体系认证证书可以在报告中查看,具体位置为报告中的质量管理体系认证证书部分.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30918",
            "question": "美新科技的质量管理体系认证证书的图片在哪里？",
            "answer": "美新科技的质量管理体系认证证书的图片可以在报告中查看,具体位置为报告中的质量管理体系认证证书部分,图片链接为https://dev-assets-api.tianhong.cn/bigdata/digital-employee/attach/img/22/4/29/29pvwskum02ngaatte6bs7ts.jpg.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30919",
            "question": "美新科技的质量管理体系认证证书的图片大小是多少？",
            "answer": "美新科技的质量管理体系认证证书的图片大小为宽180像素,高84像素.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30920",
            "question": "美新科技的质量管理体系认证证书的图片是否有边框？",
            "answer": "美新科技的质量管理体系认证证书的图片没有边框.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30921",
            "question": "美新科技的质量管理体系认证证书的图片是否有文字说明？",
            "answer": "美新科技的质量管理体系认证证书的图片没有文字说明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30922",
            "question": "美新科技的质量管理体系认证证书的图片是否有标题？",
            "answer": "美新科技的质量管理体系认证证书的图片没有标题.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30923",
            "question": "美新科技的质量管理体系认证证书的图片是否有标注来源？",
            "answer": "美新科技的质量管理体系认证证书的图片没有标注来源.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30924",
            "question": "美新科技的质量管理体系认证证书的图片是否有标注日期？",
            "answer": "美新科技的质量管理体系认证证书的图片没有标注日期.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30925",
            "question": "美新科技的质量管理体系认证证书的图片是否有标注编号？",
            "answer": "美新科技的质量管理体系认证证书的图片没有标注编号.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30926",
            "question": "美新科技的质量管理体系认证证书的图片是否有标注认证机构？",
            "answer": "美新科技的质量管理体系认证证书的图片没有标注认证机构.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30927",
            "question": "美新科技获得了哪些国内产品认证？",
            "answer": "美新科技获得了中国绿色产品认证、中国环境标识认证(十环认证)、中国绿色建材产品认证、儿童安全级产品认证、健康建材产品认证、绿色产品设计认证等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30928",
            "question": "美新科技获得了哪些国际认证？",
            "answer": "美新科技获得了美国icc-es认证、加拿大ccmc认证、新加坡green label认证、韩国生态标签、scs-翠鸟回收物质含量认证、fsc-森林认证、epd环境产品声明、leed领先能源环境设计声明、well健康建筑标准、breeam英国建筑研究院环境评估方法、hqe法国高质量环境可持续建筑认证等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30929",
            "question": "美新科技是否获得了儿童安全级产品认证？",
            "answer": "是的,美新科技获得了儿童安全级产品认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30930",
            "question": "美新科技是否获得了LEED领先能源环境设计声明认证？",
            "answer": "是的,美新科技获得了leed领先能源环境设计声明认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30931",
            "question": "美新科技是否获得了中国绿色建材产品认证？",
            "answer": "是的,美新科技获得了中国绿色建材产品认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30932",
            "question": "美新科技实施的成品质量检测模式是什么？",
            "answer": "\"美新科技实施\"\"内外部双检测\"\"模式",
            "document_uuid": "确保产品质量达到最高标准.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "30933",
            "question": "初检环节中，美新科技如何进行产品检测？",
            "answer": "在初检环节,美新科技在车间有专职人员负责在生产线对产品进行基础性的外观及尺寸检验,并将合格产品抽样送至公司实验室进行测试.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30934",
            "question": "在测试环节，美新科技对产品进行哪些性能测试？",
            "answer": "在测试环节,美新科技对产品开展多项性能测试,涵盖抗老化测试、抗弯测试、强度测试、极限测试等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30935",
            "question": "产品入库环节，美新科技如何进行二次检验？",
            "answer": "在产品入库环节,公司会再按批次将产品抽样送至实验室进行二次检验.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30936",
            "question": "美新科技如何邀请外部第三方进行产品监测？",
            "answer": "公司定期邀请外部有资质的第三方对抽样产品进行监测并出具监测报告.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30937",
            "question": "美新科技的测量管理体系认证证书编号是什么？",
            "answer": "证书编号no. cms粤[2020]aaa3125号.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30938",
            "question": "美新科技的单位地址在哪里？",
            "answer": "单位地址:惠州市惠东县大岭镇十二托乌塘地段.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30939",
            "question": "美新科技的测量管理体系覆盖的产品或业务范围是什么？",
            "answer": "测量管理体系覆盖的产品或业务范围包括产品质量、经营管理、节能降耗、环境监测等方面的测量管理体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30940",
            "question": "美新科技的测量管理体系符合哪些标准？",
            "answer": "\"测量管理体系符合gb/t 19022-2003/iso 10012:2003<测量管理体系",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "测量过程和测量设备的要求>标准的全部要求.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30941",
            "question": "美新科技的测量管理体系覆盖的地域范围是什么？",
            "answer": "测量管理体系覆盖的地域范围未具体说明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30942",
            "question": "美新科技的测量管理体系认证证书附件中包含哪些信息？",
            "answer": "证书附件中包含证书编号、单位名称、单位地址、注册地址、测量管理体系覆盖的产品或业务范围等信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30943",
            "question": "美新科技的测量管理体系认证证书附件中的单位名称是什么？",
            "answer": "单位名称是美新科技股份有限公司.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30944",
            "question": "美新科技的测量管理体系认证证书附件中的注册地址是什么？",
            "answer": "注册地址是惠州市惠东县大岭镇十二托乌塘地段.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30945",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围是什么？",
            "answer": "测量管理体系覆盖的产品或业务范围包括产品质量、经营管理、节能降耗、环境监测等方面的测量管理体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30946",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的地域范围是什么？",
            "answer": "测量管理体系覆盖的地域范围未具体说明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30947",
            "question": "美新科技的测量管理体系认证证书附件中的注意项是什么？",
            "answer": "注意项包括证书编号、单位名称、单位地址、注册地址、测量管理体系覆盖的产品或业务范围等信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30948",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围具体是什么？",
            "answer": "测量管理体系覆盖的产品或业务范围包括塑木墙板、地板制造与销售.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30949",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围是否需要相关部门批准？",
            "answer": "测量管理体系覆盖的产品或业务范围中,依法须经批准的项目,经相关部门批准后方可开展经营活动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30950",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围是否包括节能降耗？",
            "answer": "测量管理体系覆盖的产品或业务范围包括节能降耗.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30951",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围是否包括环境监测？",
            "answer": "测量管理体系覆盖的产品或业务范围包括环境监测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30952",
            "question": "美新科技的测量管理体系认证证书附件中的测量管理体系覆盖的产品或业务范围是否包括产品质量？",
            "answer": "测量管理体系覆盖的产品或业务范围包括产品质量.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30953",
            "question": "美新科技为家用客户提供多长时间的产品质保？",
            "answer": "美新科技为家用客户提供最高25年的产品质保.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30954",
            "question": "美新科技为商用客户提供多长时间的产品质保？",
            "answer": "美新科技为商用客户提供最高10年的产品质保.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30955",
            "question": "美新科技在2024年共进行了多少批次的成品抽样检测？",
            "answer": "美新科技在2024年共进行了17,122批次的成品抽样检测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30956",
            "question": "美新科技2024年的成品检测合格率是多少？",
            "answer": "美新科技2024年的成品检测合格率达到了99%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30957",
            "question": "测量管理体系认证证书的有效期至何时？",
            "answer": "测量管理体系认证证书的有效期至2025年11月12日.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30958",
            "question": "测量管理体系认证证书的颁证日期是哪一天？",
            "answer": "测量管理体系认证证书的颁证日期是2020年11月13日.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30959",
            "question": "测量管理体系认证证书的颁证部门是哪家公司？",
            "answer": "测量管理体系认证证书的颁证部门是中启计量体系认证有限公司.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30960",
            "question": "测量管理体系认证证书的签发人是谁？",
            "answer": "测量管理体系认证证书的签发人信息未在文本中明确给出.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30961",
            "question": "本报告包含哪些主要内容？",
            "answer": "\"本报告包含董事长致辞、关于美新科技、可持续发展方针、绿色生态",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "环境篇、和谐共融",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "社会篇、精业笃行",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "治理篇和附录等内容.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30962",
            "question": "美新科技在质量与安全文化方面做了哪些工作？",
            "answer": "美新科技持续深化产品质量与安全文化建设,实施了一系列多层次、多维度的宣贯与教育活动,包括新入职员工质量安全培训和常态化日常质量与安全培训.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30963",
            "question": "2024年美新科技在质量与安全文化方面有哪些具体措施？",
            "answer": "2024年,美新科技品管部策划并实施了一系列多层次、多维度的宣贯与教育活动,包括新入职员工质量安全培训和常态化日常质量与安全培训.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30964",
            "question": "美新科技为何要深化产品质量与安全文化建设？",
            "answer": "美新科技深化产品质量与安全文化建设是为了全面提升员工的质量安全意识及产品质量管理能力,致力于打造卓越的质量文化氛围.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30965",
            "question": "美新科技的可持续发展方针包括哪些方面？",
            "answer": "\"美新科技的可持续发展方针包括绿色生态",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "环境篇、和谐共融",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "社会篇和精业笃行",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "治理篇.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30966",
            "question": "美新科技的绿色生态·环境篇主要关注什么？",
            "answer": "\"美新科技的绿色生态",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "环境篇主要关注环境保护和可持续发展.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "30967",
            "question": "美新科技的和谐共融·社会篇主要关注什么？",
            "answer": "\"美新科技的和谐共融",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "社会篇主要关注企业与社会的和谐共融",
            "question": "包括社会责任和社区贡献.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "30968",
            "question": "美新科技的精业笃行·治理篇主要关注什么？",
            "answer": "\"美新科技的精业笃行",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "治理篇主要关注企业治理和管理",
            "question": "包括公司治理结构和管理实践.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "30969",
            "question": "美新科技的附录部分可能包含哪些内容？",
            "answer": "美新科技的附录部分可能包含一些补充资料,如相关数据、图表、参考文献等,以提供更全面的信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30970",
            "question": "年度质量提升专项培训的目的是什么？",
            "answer": "旨在强化部门员工对质量标准的理解与执行能力,进一步增强员工对产品质量与安全的重视程度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30971",
            "question": "品管部对新入职员工实施的培训计划目的是什么？",
            "answer": "确保新员工在正式开展工作前具备扎实的专业知识和实践能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30972",
            "question": "新入职员工需要经过多长时间的培训期？",
            "answer": "新入职员工需经过至少一个月的培训期.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30973",
            "question": "新入职员工在培训期间需要熟悉哪些内容？",
            "answer": "新入职员工需要熟悉并掌握日常工作内容及操作规范,深入了解现场及区域环境的安全要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30974",
            "question": "新入职员工在通过培训考核后可以做什么？",
            "answer": "在通过品质部检验要求培训考核后方可正式上岗.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30975",
            "question": "美新科技设立了哪些部门来支持客户服务？",
            "answer": "美新科技设立了售后服务部门,并建立客户服务热线和包括官网.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30976",
            "question": "品管部对新入职员工的培训依据是什么？",
            "answer": "根据部门制定的<岗位安全查检表>.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30977",
            "question": "年度质量提升专项培训的目标群体是谁？",
            "answer": "年度质量提升专项培训的目标群体是部门员工.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30978",
            "question": "新入职员工在培训期间需要掌握哪些技能？",
            "answer": "新入职员工需要掌握日常工作内容及操作规范,了解现场及区域环境的安全要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30979",
            "question": "美新科技的客户服务热线和官网的作用是什么？",
            "answer": "美新科技的客户服务热线和官网用于提供客户服务支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30980",
            "question": "年度质量提升专项培训的目的是为了什么？",
            "answer": "目的是为了强化部门员工对质量标准的理解与执行能力,进一步增强员工对产品质量与安全的重视程度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30981",
            "question": "新入职员工在培训期间需要完成哪些任务？",
            "answer": "新入职员工需要熟悉并掌握日常工作内容及操作规范,深入了解现场及区域环境的安全要求,并通过品质部检验要求培训考核.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30982",
            "question": "美新科技的售后服务部门主要负责什么？",
            "answer": "美新科技的售后服务部门主要负责提供售后服务支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30983",
            "question": "美新科技通过哪些渠道收集客户反馈？",
            "answer": "美新科技通过电子邮件、400电话及社交媒体等多元化的沟通渠道收集客户反馈.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30984",
            "question": "美新科技多久进行一次顾客满意度调查？",
            "answer": "美新科技每两年进行一次顾客满意度调查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30985",
            "question": "2024年美新科技客户满意度调查覆盖了多少家企业？",
            "answer": "2024年美新科技共针对39家客户企业开展客户满意度调查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30986",
            "question": "2024年美新科技客户满意度是多少？",
            "answer": "2024年美新科技客户满意度达95%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30987",
            "question": "美新科技2024年的客户投诉解决率是多少？",
            "answer": "2024年美新科技客户投诉解决率为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30988",
            "question": "美新科技在质量管理方面设定了哪些目标？",
            "answer": "美新科技在质量管理方面设定了明确的目标:来料合格率≥98%,成品合格率≥99%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30989",
            "question": "美新科技推行了什么制度以确保质量问题的及时发现与处理？",
            "answer": "美新科技推行了线上反馈制度,确保生产过程中质量问题的及时发现与处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30990",
            "question": "截至报告期，美新科技是否发生过因产品和服务导致的重大客户健康与安全事件？",
            "answer": "截至报告期,美新科技未发生任何因产品和服务导致的重大客户健康与安全事件.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30991",
            "question": "2024年美新科技产品和服务相关的安全与质量重大责任事故总数是多少？",
            "answer": "2024年美新科技产品和服务相关的安全与质量重大责任事故总数为0件.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30992",
            "question": "美新科技产品和服务相关的安全与质量重大责任事故相关经济损失总额是多少？",
            "answer": "美新科技产品和服务相关的安全与质量重大责任事故相关经济损失总额未给出具体数值.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30993",
            "question": "美新科技的顾客满意度调查涵盖哪些内容？",
            "answer": "美新科技的顾客满意度调查涵盖对销售人员的服务质量评价、对产品质量及售后服务的评价和建议、投诉处理结果的满意程度等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30994",
            "question": "美新科技如何确保质量问题的及时发现与处理？",
            "answer": "美新科技通过推行线上反馈制度确保质量问题的及时发现与处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30995",
            "question": "美新科技是否发生过重大客户健康与安全事件？",
            "answer": "截至报告期,美新科技未发生任何因产品和服务导致的重大客户健康与安全事件.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30996",
            "question": "美新科技的客户满意度调查频率是多久一次？",
            "answer": "美新科技每两年进行一次顾客满意度调查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30997",
            "question": "美新科技的客户满意度调查覆盖了哪些方面？",
            "answer": "美新科技的客户满意度调查覆盖了对销售人员的服务质量评价、对产品质量及售后服务的评价和建议、投诉处理结果的满意程度等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30998",
            "question": "美新科技的客户满意度调查结果如何？",
            "answer": "2024年美新科技共针对39家客户企业开展客户满意度调查,客户满意度达95%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "30999",
            "question": "美新科技的客户投诉解决率是多少？",
            "answer": "2024年美新科技客户投诉解决率为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31000",
            "question": "美新科技在信息安全和隐私保护方面采取了哪些措施？",
            "answer": "美新科技通过物理性管理、网络分离管理、访问管理、备份管理和数据库管理等措施,确保设备、网络、系统及数据的安全.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31001",
            "question": "美新科技如何确保报废电脑的安全处理？",
            "answer": "报废电脑需由it部对存储媒体进行重复格式化,再交由合规认证的机构回收处理,并由相关机构提供回收证明.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31002",
            "question": "美新科技的网络分离管理是如何实施的？",
            "answer": "网络分离管理通过独立平台开发和运营数据库网络隔离,确保开发人员和业务人员仅能访问各自数据库,避免数据库错连.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31003",
            "question": "美新科技如何管理电脑的访问权限？",
            "answer": "每台电脑安装端点管理系统(kaspersky end point-kep),所有电脑均通过kep服务器下发的管理政策进行使用,确保准确发放权限.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31004",
            "question": "美新科技如何进行数据备份？",
            "answer": "定期对数据库进行备份,进行备份复查和备份数据恢复测试,确保备份数据可以恢复和使用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31005",
            "question": "美新科技如何提升员工的信息安全意识？",
            "answer": "公司定期组织信息安全培训,培训内容涵盖数据安全基础知识、信息泄漏风险防范等,确保新员工能够快速掌握信息安全的核心要领.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31006",
            "question": "美新科技如何进行漏洞检测？",
            "answer": "美新科技通过外部第三方进行网络及系统漏洞检测,覆盖网络架构、系统权限、数据存储及传输等关键环节,帮助及时发现并修复安全隐患.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31007",
            "question": "美新科技如何进行攻防演练？",
            "answer": "通过模拟真实攻击场景,聚焦业务数据安全风险,识别潜在漏洞和薄弱环节,确保业务数据的全生命周期安全.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31008",
            "question": "美新科技的信息安全等级保护认证进展如何？",
            "answer": "根据<信息安全技术 网络安全等级保护定级指南>(gb/t 222402020)的规定,公司正积极开展信息安全等级保护三级认证,进一步提升信息系统的安全防护能力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31009",
            "question": "2024年度，美新科技对信息安全相关人员开展了多少次培训？",
            "answer": "2024年度,美新科技对信息安全相关人员开展了88次培训.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31010",
            "question": "2024年度，美新科技培训参与人数是多少？",
            "answer": "2024年度,美新科技培训参与人数为273人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31011",
            "question": "2024年度，美新科技的培训覆盖率是多少？",
            "answer": "2024年度,美新科技的培训覆盖率为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31012",
            "question": "2024年度，美新科技发生数据安全和信息泄漏事件多少次？",
            "answer": "2024年度,美新科技发生数据安全和信息泄漏事件0次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31013",
            "question": "2024年度，美新科技数据安全事件导致的经济损失总额是多少？",
            "answer": "2024年度,美新科技数据安全事件导致的经济损失总额为0万元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31014",
            "question": "美新科技如何确保供应链各环节符合环境保护、社会责任和公司治理的要求？",
            "answer": "美新科技通过严格的供应商准入标准和评估机制,对供应商进行全方位、体系化且规范化的管控,确保供应链各环节符合环境保护、社会责任和公司治理的要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31015",
            "question": "美新科技在供应商管理中如何进行前期调研？",
            "answer": "美新科技在前期调研阶段,采购部会通过背景调查及电话调查等方式对待选供应商资质、认证情况、行政处罚等信息进行审核,确保供应商符合公司制定的相关标准,并由技术部对供应商提供的产品样品进行性能测试.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31016",
            "question": "美新科技如何进行供应商现场审核？",
            "answer": "\"美新科技在供应商现场审核阶段",
            "document_uuid": "全面核查供应商在环境、社会及合规运营方面的实际表现.",
            "release_status": ""
        },
        {
            "id": "在治理层面重点关注供应商的合规性文件、质量管理体系等",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "在环保层面重点关注环保设施运行情况、废弃物处理流程等",
            "question": "",
            "answer": "",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "在社会层面重点关注供应商用工情况、劳工权益等.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "31017",
            "question": "美新科技如何进行供应商绩效考核？",
            "answer": "美新科技定期对供应商开展绩效考核,通过内部建立的<供应商评审的评分表>进行评估打分,针对存在的不合格项,将主动与供应商进行沟通协商,协助供应商进行整改和优化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31018",
            "question": "美新科技的AEO管理体系为公司带来了什么保障？",
            "answer": "美新科技通过了aeo(authorized economic operator)高级企业认证,为公司的全球供应链安全与高效运作提供了有力保障.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31019",
            "question": "美新科技如何保障供应链的安全性和稳定性？",
            "answer": "美新科技通过构建多元化供应链体系,积极拓展全球供应商网络,避免对单一供应商或地区的过度依赖,确保原材料和关键材料的稳定供应.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31020",
            "question": "美新科技如何拓展全球供应商网络？",
            "answer": "美新科技积极拓展全球供应商网络,与多家优质供应商建立长期合作关系,确保原材料和关键材料的稳定供应.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31021",
            "question": "美新科技如何管理经销商？",
            "answer": "美新科技对经销商进行严格的审核及评估,从多个维度进行评估,并由销售总监前往经销商所在地进行实地考察.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31022",
            "question": "美新科技在销售阶段如何监控经销商？",
            "answer": "美新科技对经销商的订单量进行详细的记录,并监测评估经销商在各方面的表现.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31023",
            "question": "美新科技为何要对经销商进行严格的审核及评估？",
            "answer": "美新科技对经销商进行严格的审核及评估是为了确保经销商满足公司的相关要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31024",
            "question": "美新科技的供应链体系有何特点？",
            "answer": "美新科技的供应链体系特点是多元化,有效保障了供应链的安全性和稳定性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31025",
            "question": "美新科技如何确保原材料和关键材料的稳定供应？",
            "answer": "美新科技通过构建多元化供应链体系,积极拓展全球供应商网络,与多家优质供应商建立长期合作关系,确保原材料和关键材料的稳定供应.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31026",
            "question": "美新科技的销售模式是什么？",
            "answer": "美新科技主要采用以自有品牌代理经销商渠道进行销售.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31027",
            "question": "美新科技在经销商筛选阶段如何进行评估？",
            "answer": "美新科技在经销商筛选阶段从多个维度对经销商进行评估,并由销售总监前往经销商所在地进行实地考察.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31028",
            "question": "美新科技如何处理经销商违反公司要求的行为？",
            "answer": "美新科技在销售阶段监测评估经销商在各方面的表现,如在合作期间出现违反公司要求的行为,会进行相应的处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31029",
            "question": "美新科技的多元化供应链体系包括哪些方面？",
            "answer": "美新科技的多元化供应链体系包括积极拓展全球供应商网络,避免对单一供应商或地区的过度依赖,与多家优质供应商建立长期合作关系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31030",
            "question": "美新科技如何确保经销商满足公司的要求？",
            "answer": "美新科技通过在多个阶段对经销商开展严格的审核及评估,确保经销商满足公司的要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31031",
            "question": "美新科技的供应链体系为何要多元化？",
            "answer": "美新科技的供应链体系多元化是为了有效保障供应链的安全性和稳定性,避免对单一供应商或地区的过度依赖.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31032",
            "question": "美新科技如何确保经销商在合作期间的表现？",
            "answer": "美新科技在销售阶段对经销商的订单量进行详细的记录,并监测评估经销商在各方面的表现.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31033",
            "question": "美新科技如何确保供应链的稳定性？",
            "answer": "美新科技通过构建多元化供应链体系,积极拓展全球供应商网络,与多家优质供应商建立长期合作关系,确保供应链的稳定性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31034",
            "question": "公司如何与经销商终止协议？",
            "answer": "公司将立即与经销商终止协议,以维护公司形象并保障消费者的权益不受侵害.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31035",
            "question": "美新科技如何赋能经销商？",
            "answer": "美新科技提供定制化线上视频培训和线下产品培训,并邀请经销商前往公司参观.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31036",
            "question": "公司多久举办一次全球代理商大会？",
            "answer": "公司每1-2年举办一次全球代理商大会.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31037",
            "question": "公司如何降低采购运输过程中的温室气体排放？",
            "answer": "公司在内部试行本地化采购政策,在同等条件下优先选择周边300公里以内的供应商.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31038",
            "question": "公司对供应商有哪些环保要求？",
            "answer": "公司要求所有供应商签署<供应商环保协议>,并明确要求其遵守协议中的相关规定,包括遵守所有国家、地方和行业特定的环境保护法律法规、鼓励使用无污染或污染较少的生产流程和设备、优先使用可回收包装材料等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31039",
            "question": "公司在供应商筛选过程中考虑哪些因素？",
            "answer": "公司在供应商筛选过程中纳入环境社会及治理相关因素的评估.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31040",
            "question": "公司对大型供应商有哪些额外要求？",
            "answer": "公司对部分大型供应商提出包括环境管理体系认证(如iso 14001)等要求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31041",
            "question": "公司获得了哪些认证？",
            "answer": "公司已获得由sgs全球服务颁授的scs回收认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31042",
            "question": "FSC产销监管链认证是由哪个机构颁发的？",
            "answer": "fsc产销监管链认证是由中国香港sgs颁发的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31043",
            "question": "美新科技在可持续采购方面取得了什么成效？",
            "answer": "美新科技在可持续采购方面取得了卓越成效.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31044",
            "question": "美新科技的企业治理核心准则之一是什么？",
            "answer": "美新科技的企业治理核心准则之一是\"以人为本\".",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31045",
            "question": "美新科技构建的可持续发展生态的基石是什么？",
            "answer": "美新科技构建的可持续发展生态的基石是以平等合规为基石.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31046",
            "question": "美新科技构建的可持续发展生态的引擎是什么？",
            "answer": "美新科技构建的可持续发展生态的引擎是人才发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31047",
            "question": "美新科技构建的可持续发展生态的纽带是什么？",
            "answer": "美新科技构建的可持续发展生态的纽带是员工参与.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31048",
            "question": "美新科技构建的可持续发展生态的底线是什么？",
            "answer": "美新科技构建的可持续发展生态的底线是安全生产.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31049",
            "question": "美新科技通过什么体系营造和谐、积极的企业文化？",
            "answer": "美新科技通过完善的薪酬和福利体系、丰富的员工关怀与活动、坚实的职业健康与安全保障营造和谐、积极的企业文化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31050",
            "question": "美新科技如何增强员工的归属感和认同感？",
            "answer": "美新科技通过营造和谐、积极的企业文化来增强员工的归属感和认同感.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31051",
            "question": "美新科技如何激发员工的创造力和工作热情？",
            "answer": "美新科技通过营造和谐、积极的企业文化来激发员工的创造力和工作热情.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31052",
            "question": "美新科技严格遵守哪些法律法规？",
            "answer": "美新科技严格遵守<中华人民共和国劳动法>、<中华人民共和国劳动合同法>、<中华人民共和国社会保险法>等法律法规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31053",
            "question": "美新科技制定了一系列的内部规章制度，具体包括哪些？",
            "answer": "美新科技制定了一系列的内部规章制度,具体包括<入职管理规范>、<培训管理规范>、<薪酬绩效管理制度>等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31054",
            "question": "美新科技如何保障员工的合法权益？",
            "answer": "美新科技通过制定一系列的内部规章制度,保障员工在合规招聘、劳动合同、培训与发展及职业健康与安全等层面的合法权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31055",
            "question": "美新科技的薪酬和福利体系是否完善？",
            "answer": "美新科技的薪酬和福利体系是完善的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31056",
            "question": "美新科技是否提供丰富的员工关怀与活动？",
            "answer": "美新科技提供丰富的员工关怀与活动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31057",
            "question": "美新科技是否提供坚实的职业健康与安全保障？",
            "answer": "美新科技提供坚实的职业健康与安全保障.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31058",
            "question": "美新科技的企业文化是否和谐、积极？",
            "answer": "美新科技的企业文化是和谐、积极的.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31059",
            "question": "美新科技的企业文化是否能激发员工的创造力和工作热情？",
            "answer": "美新科技的企业文化能激发员工的创造力和工作热情.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31060",
            "question": "公司为员工提供了哪些福利措施？",
            "answer": "公司为员工提供五险一金、免费食宿、带薪休假、健康体检及节日慰问等一系列福利措施.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31061",
            "question": "公司如何实现员工与企业的共同发展？",
            "answer": "公司通过提供一系列福利措施,使员工感受到尊重与关爱,从而实现员工与企业的共同发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31062",
            "question": "美新科技的招聘机制是什么？",
            "answer": "美新科技通过线上线下和内外部招聘双轨并行的招聘机制为多元化人才提供平等的就业机会.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31063",
            "question": "美新科技为退伍军人和残障人士提供了哪些支持？",
            "answer": "美新科技积极为退伍军人及残障人士创造就业机会,提供必要的培训和合适的岗位,给予充分的包容与支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31064",
            "question": "截至报告期，美新科技为多少退伍军人和残障人士提供了就业岗位？",
            "answer": "截至报告期,美新科技共计为7名退伍军人和4名残障人士提供了就业岗位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31065",
            "question": "在招聘流程中，公司如何保障员工权益？",
            "answer": "在招聘流程中,公司严格恪守劳动法相关要求,制定<入职签署资料清单>,要求员工签署一系列规范和制度文件,以保障员工权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31066",
            "question": "公司要求员工签署哪些文件？",
            "answer": "公司要求员工签署包括劳动合同、员工行为规范实施细则、保密协议、知识产权声明、考勤管理制度等一系列规范和制度文件.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31067",
            "question": "美新科技制定了哪些政策文件来保护员工权益？",
            "answer": "美新科技制定了<拯救童工和保护未成年工程序>和<禁止强迫劳动程序>政策文件,严令禁止在公司内部使用童工的行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31068",
            "question": "公司如何确保招聘流程的公平性？",
            "answer": "公司通过线上线下和内外部招聘双轨并行的招聘机制,为多元化人才提供平等的就业机会,确保招聘流程的公平性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31069",
            "question": "公司如何对待退伍军人和残障人士？",
            "answer": "公司积极为退伍军人及残障人士创造就业机会,提供必要的培训和合适的岗位,给予充分的包容与支持.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31070",
            "question": "公司如何确保员工的工作体验？",
            "answer": "公司通过提供一系列福利措施,使员工真切感受到尊重与关爱,从而确保员工的工作体验.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31071",
            "question": "公司如何保障员工的合法权益？",
            "answer": "公司通过制定<入职签署资料清单>,要求员工签署一系列规范和制度文件,切实保障员工的合法权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31072",
            "question": "公司如何对待未成年工？",
            "answer": "公司制定了<拯救童工和保护未成年工程序>政策文件,以保护未成年工的权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31073",
            "question": "公司如何对待童工？",
            "answer": "公司制定了<拯救童工和保护未成年工程序>政策文件,严令禁止在公司内部使用童工的行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31074",
            "question": "公司如何对待强迫劳动？",
            "answer": "公司制定了<禁止强迫劳动程序>政策文件,严令禁止在公司内部使用强迫劳动的行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31075",
            "question": "公司如何确保员工的健康？",
            "answer": "公司为员工提供健康体检等福利措施,确保员工的健康.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31076",
            "question": "公司如何对待员工的节日？",
            "answer": "公司为员工提供节日慰问等福利措施,使员工在节日中感受到公司的关爱.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31077",
            "question": "公司如何对待员工的休息？",
            "answer": "公司为员工提供带薪休假等福利措施,确保员工的休息权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31078",
            "question": "公司如何对待员工的住房问题？",
            "answer": "公司为员工提供免费食宿等福利措施,解决员工的住房问题.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31079",
            "question": "公司如何对待员工的保险问题？",
            "answer": "公司为员工提供五险一金等福利措施,确保员工的保险权益.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31080",
            "question": "公司如何从源头杜绝童工雇佣现象？",
            "answer": "公司通过在招聘前进行全面的员工背景调查及招聘过程中身份验证等手段从源头杜绝童工雇佣的现象.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31081",
            "question": "如果发现公司内部存在雇佣童工的行为，公司会如何处理？",
            "answer": "一旦发现公司内部存在雇佣童工的行为,将立即向人力资源及行政主管部门负责人或总经理报告,严格处理相关人员并及时采取必要的补救措施.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31082",
            "question": "公司为员工提供了哪些活动来增强团队凝聚力？",
            "answer": "公司全年组织多场节日庆祝活动,还邀请员工家属参与,旨在增强团队凝聚力,营造积极向上的企业文化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31083",
            "question": "公司为何要开展员工活动、员工关爱及员工沟通的举措？",
            "answer": "公司开展这些举措旨在增强团队凝聚力,营造积极向上的企业文化,让员工放松身心,创造与同事交流互动的机会,助力培育团队意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31084",
            "question": "公司如何通过活动来提升员工的幸福感？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与等方式,让员工放松身心,增强与同事的交流互动,提升员工的幸福感.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31085",
            "question": "公司如何体现对员工的关怀？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,体现对员工的关怀.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31086",
            "question": "公司如何通过活动来增强员工的归属感？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,增强员工的归属感.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31087",
            "question": "公司如何通过活动来提升员工的工作积极性？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,提升员工的工作积极性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31088",
            "question": "公司如何通过活动来促进员工之间的交流？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,促进员工之间的交流.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31089",
            "question": "公司如何通过活动来提升员工的团队意识？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,提升员工的团队意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31090",
            "question": "公司如何通过活动来增强员工的组织凝聚力？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,增强员工的组织凝聚力.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31091",
            "question": "公司如何通过活动来提升员工的工作满意度？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,提升员工的工作满意度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31092",
            "question": "公司如何通过活动来提升员工的工作效率？",
            "answer": "公司通过组织节日庆祝活动、邀请员工家属参与、开展员工关爱及员工沟通的举措,提升员工的工作效率.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31093",
            "question": "美新科技在哪一天举办了花园烧烤主题活动？",
            "answer": "2024年1月12日",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31094",
            "question": "美新科技的烧烤活动在哪里举办？",
            "answer": "在公司园区内",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31095",
            "question": "美新科技的烧烤活动有哪些特色？",
            "answer": "活动包括烧烤、才艺展示等,点燃了参与者的热情",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31096",
            "question": "美新科技的员工福利计划包括哪些内容？",
            "answer": "包括职业健康体检、免费运动设施、免费餐饮及住宿、住房补贴、劳动防护用品、工作服、节日福利、旅游福利、雇主责任险、社会保险、住房公积金等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31097",
            "question": "美新科技为员工提供哪些运动设施？",
            "answer": "包括健身房、篮球场、网球场等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31098",
            "question": "美新科技为外宿员工提供什么补贴？",
            "answer": "提供住房补贴",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31099",
            "question": "美新科技为员工提供哪些工作服？",
            "answer": "免费提供足量的夏装和冬装工作服",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31100",
            "question": "美新科技为员工提供哪些常规福利？",
            "answer": "包括节日福利、旅游福利等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31101",
            "question": "美新科技为员工提供哪些基础保障？",
            "answer": "包括雇主责任险、社会保险、住房公积金等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31102",
            "question": "美新科技的烧烤活动体现了什么精神？",
            "answer": "体现了员工之间的团结和共享欢乐的精神",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31103",
            "question": "美新科技的烧烤活动有哪些活动内容？",
            "answer": "包括烧烤、才艺展示等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31104",
            "question": "美新科技的烧烤活动在什么环境下进行？",
            "answer": "在花园烧烤的环境中进行",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31105",
            "question": "美新科技的烧烤活动展示了员工的什么特点？",
            "answer": "展示了员工自信大方的特点",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31106",
            "question": "美新科技的烧烤活动体现了员工之间的什么关系？",
            "answer": "体现了员工之间不仅是同事,更是共享欢乐的一家人",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31107",
            "question": "美新科技的烧烤活动是如何点燃参与者的热情的？",
            "answer": "通过炭火的热度与美食的香气交织,点燃了参与者的热情",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31108",
            "question": "美新科技的烧烤活动在什么时间进行？",
            "answer": "在2024年1月12日进行",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31109",
            "question": "美新科技的烧烤活动有哪些展示？",
            "answer": "展示了员工的才艺",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31110",
            "question": "美新科技的烧烤活动有哪些设施？",
            "answer": "包括烧烤设施、舞台等",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31111",
            "question": "美新科技的烧烤活动有哪些参与者？",
            "answer": "包括美新科技的同事们",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31112",
            "question": "美新科技的烧烤活动有哪些展示内容？",
            "answer": "展示了员工的才艺",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31113",
            "question": "美新科技的烧烤活动有哪些展示形式？",
            "answer": "包括才艺展示",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31114",
            "question": "美新科技的烧烤活动有哪些展示地点？",
            "answer": "在星光舞台下进行",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31115",
            "question": "美新科技的烧烤活动有哪些展示方式？",
            "answer": "通过才艺展示的方式",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31116",
            "question": "公司为女性员工提供了哪些特殊保护措施？",
            "answer": "\"公司特别制定了<妇女\"\"三期\"\"保护规定>和<孕妇岗位风险评估程序>等保护措施",
            "document_uuid": "全面保障女性员工在孕期、产期和哺乳期的健康与权益.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "31117",
            "question": "公司为女性员工提供了哪些假期？",
            "answer": "公司为女性员工提供婚假、产假、育儿假等假期.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31118",
            "question": "公司是否为孕妇设立了独立的休息场所？",
            "answer": "是的,公司还在工作现场设立了孕妇独立的休息场所.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31119",
            "question": "公司成立了什么组织来支持员工？",
            "answer": "公司成立了员工工会,向公司提出合理化建议,并通过工会为困难员工提供支持与帮助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31120",
            "question": "员工在什么情况下可以申请补助？",
            "answer": "在家属重疾等特殊情况下,员工可以申请补助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31121",
            "question": "工会如何帮助困难员工？",
            "answer": "工会会组织募捐活动,为困难员工提供经济上的援助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31122",
            "question": "公司如何保障女性员工的权益？",
            "answer": "\"公司通过制定<妇女\"\"三期\"\"保护规定>和<孕妇岗位风险评估程序>等措施",
            "document_uuid": "保障女性员工的权益.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "31123",
            "question": "公司是否重视与员工的沟通？",
            "answer": "是的,美新科技高度重视与员工的沟通交流,全方位搭建与员工开展良好沟通的桥梁.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31124",
            "question": "公司为女性员工提供了哪些法律保障？",
            "answer": "公司严格按照法律法规,为女性员工提供婚假、产假、育儿假等假期.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31125",
            "question": "公司如何支持困难员工？",
            "answer": "公司通过员工工会为困难员工提供支持与帮助,并在特殊情况下提供补助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31126",
            "question": "公司是否关注员工的健康？",
            "answer": "是的,公司特别关注女性员工在孕期、产期和哺乳期的健康.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31127",
            "question": "公司是否鼓励员工提出建议？",
            "answer": "是的,公司通过员工工会向公司提出合理化建议.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31128",
            "question": "公司是否提供经济援助给困难员工？",
            "answer": "是的,工会会组织募捐活动,为困难员工提供经济上的援助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31129",
            "question": "公司是否设立了孕妇休息场所？",
            "answer": "是的,公司还在工作现场设立了孕妇独立的休息场所.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31130",
            "question": "公司是否为女性员工提供法律规定的假期？",
            "answer": "是的,公司为女性员工提供婚假、产假、育儿假等假期.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31131",
            "question": "公司是否成立了工会来支持员工？",
            "answer": "是的,公司成立了员工工会,为困难员工提供支持与帮助.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31132",
            "question": "公司是否关注女性员工的特殊需求？",
            "answer": "\"是的",
            "document_uuid": "公司特别制定了<妇女\"\"三期\"\"保护规定>和<孕妇岗位风险评估程序>等措施",
            "release_status": "全面保障女性员工的特殊需求.\"",
            "": "qa_await"
        },
        {
            "id": "31133",
            "question": "公司是否为员工提供沟通渠道？",
            "answer": "是的,美新科技高度重视与员工的沟通交流,全方位搭建与员工开展良好沟通的桥梁.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31134",
            "question": "美新科技如何确保员工的合法权益？",
            "answer": "美新科技通过制定内部<员工意见、建议、申诉及反馈管理程序>,搭建线上和线下的双沟通渠道,确保员工可以通过多种方式反馈意见、投诉和举报.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31135",
            "question": "美新科技的沟通渠道有哪些？",
            "answer": "美新科技已搭建线上和线下的双沟通渠道,员工可以通过工厂内设立的员工意见箱,拨打员工投诉热线电话,向部门或区域员工代表口头投诉等方式反馈意见、投诉和举报.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31136",
            "question": "美新科技如何进行员工培训？",
            "answer": "美新科技制定了<员工培训控制程序>,从多个方面规范员工培训流程,确保培训工作的科学性、规范性和有效性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31137",
            "question": "美新科技的通用培训内容有哪些？",
            "answer": "通用培训内容包括企业文化、员工手册、知识产权声明、安全生产及职业健康、企业内部政策及规章制定等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31138",
            "question": "美新科技的专项培训内容有哪些？",
            "answer": "专项培训内容包括技术技能提升、上岗前操作培训、安全与职工培训、体系要求培训、能力发展培训等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31139",
            "question": "美新科技如何进行员工晋升？",
            "answer": "美新科技构建了一套从普通员工到班组长、主任、经理,直至总监的覆盖全员的培养体系,通过系统的培训课程、岗位轮换、组长和班长带教等方式,帮助员工不断提升专业技能、管理能力和综合素质.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31140",
            "question": "美新科技的职称评定计划覆盖哪些部门？",
            "answer": "美新科技的职称评定计划优先覆盖研发和生产部门的核心管理人员.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31141",
            "question": "美新科技如何表彰优秀员工？",
            "answer": "\"美新科技每年组织开展评优表彰大会",
            "document_uuid": "对优秀员工进行表彰.",
            "release_status": ""
        },
        {
            "id": "2024年",
            "question": "美新科技评优颁奖典礼设置了包括优秀员工、优秀管理者、查患排险能手等诸多奖项.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "31142",
            "question": "美新科技的员工投诉及举报调查解决率是多少？",
            "answer": "美新科技2024年员工投诉及举报调查解决率为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31143",
            "question": "美新科技的员工总数是多少？",
            "answer": "截至2024年末,美新科技共有员工905人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31144",
            "question": "美新科技如何确保员工的劳动合同签订和五险一金的全覆盖？",
            "answer": "美新科技确保员工劳动合同签订和五险一金100%全覆盖,切实保障员工的合法权益和尊严.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31145",
            "question": "美新科技的培训体系包括哪些方面？",
            "answer": "美新科技的培训体系包括通用培训和专项培训两个维度,通用培训涵盖企业文化、员工手册、知识产权声明、安全生产及职业健康等内容,专项培训则针对不同部门和岗位的专业需求.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31146",
            "question": "美新科技的通用培训面向哪些员工？",
            "answer": "美新科技的通用培训面向新入职员工和全体员工,内容包括企业文化、员工手册、知识产权声明、安全生产及职业健康等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31147",
            "question": "美新科技的专项培训面向哪些员工？",
            "answer": "美新科技的专项培训面向岗位员工,内容包括技术技能提升、上岗前操作培训、安全与职工培训、体系要求培训、能力发展培训等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31148",
            "question": "美新科技如何确保培训工作的有效性？",
            "answer": "美新科技通过书面和口头考核的方式对员工培训成效进行检验,确保培训工作的有效性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31149",
            "question": "美新科技的培训体系中有哪些具体的培训内容？",
            "answer": "美新科技的培训体系中包括通用制度培训、生产安全培训、环保安全培训、职业健康安全、知识产权培训、反贪腐培训、社会责任培训、iso体系培训、危废管理知识培训、部门岗前培训、msds知识培训、iso内审员培训等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31150",
            "question": "美新科技如何进行员工的职业发展指导？",
            "answer": "美新科技通过系统的培训课程、岗位轮换、组长和班长带教等方式,帮助员工不断提升专业技能、管理能力和综合素质,为员工提供清晰的职业发展路径.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31151",
            "question": "美新科技如何识别和培养高潜力人才？",
            "answer": "美新科技通过职称评定计划帮助管理层人员明确自身的职业发展方向,同时也有助于公司识别和培养高潜力人才,为未来的战略发展储备核心力量.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31152",
            "question": "美新科技如何确保员工的职业道德素养？",
            "answer": "美新科技通过通用培训中的反贪腐培训和社会责任培训等内容,帮助员工提升职业道德素养,增强社会责任感.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31153",
            "question": "美新科技如何确保员工的安全生产？",
            "answer": "美新科技通过通用培训中的安全生产及职业健康培训,以及专项培训中的在岗安全培训,确保员工的安全生产.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31154",
            "question": "美新科技如何确保员工的职业健康？",
            "answer": "美新科技通过通用培训中的职业健康安全培训,以及专项培训中的职业健康安全培训,确保员工的职业健康.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31155",
            "question": "美新科技如何确保员工的环保意识？",
            "answer": "美新科技通过通用培训中的环保安全培训,以及专项培训中的危废管理知识培训,确保员工的环保意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31156",
            "question": "美新科技如何确保员工的知识产权意识？",
            "answer": "美新科技通过通用培训中的知识产权培训,确保员工的知识产权意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31157",
            "question": "2024年末美新科技的在职员工总数是多少？",
            "answer": "2024年末美新科技的在职员工总数为905人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31158",
            "question": "美新科技母公司和子公司的在职员工数分别是多少？",
            "answer": "美新科技母公司在职员工数为806人,子公司为99人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31159",
            "question": "美新科技的员工按岗位分类，各类岗位的员工数分别是多少？",
            "answer": "美新科技的员工按岗位分类,生产人员为601人,销售人员为69人,技术人员(含研发)为127人,财务人员为19人,行政人员为89人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31160",
            "question": "美新科技的员工按学历分类，各类学历的员工数分别是多少？",
            "answer": "美新科技的员工按学历分类,本科及以上学历的员工数为106人,大专学历的员工数为103人,中专及以下学历的员工数为696人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31161",
            "question": "美新科技的员工流失率是多少？",
            "answer": "\"美新科技的员工流失率为",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "7.94%.\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "31162",
            "question": "美新科技劳动合同签订比例是多少？",
            "answer": "美新科技劳动合同签订比例为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31163",
            "question": "美新科技员工五险一金覆盖比例是多少？",
            "answer": "美新科技员工五险一金覆盖比例为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31164",
            "question": "美新科技劳动诉讼、仲裁与员工纠纷案件数量是多少？",
            "answer": "美新科技劳动诉讼、仲裁与员工纠纷案件数量为2起.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31165",
            "question": "美新科技劳动诉讼、仲裁与员工纠纷案件解决率是多少？",
            "answer": "美新科技劳动诉讼、仲裁与员工纠纷案件解决率为50%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31166",
            "question": "美新科技员工培训人次是多少？",
            "answer": "美新科技员工培训人次为5,702次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31167",
            "question": "美新科技员工培训总投入金额是多少？",
            "answer": "美新科技员工培训总投入金额为66,796.21元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31168",
            "question": "2024年新入职员工培训参与人数是多少？",
            "answer": "2024年新入职员工培训参与人数为273人,每人培训时长超过24小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31169",
            "question": "2024年在岗安全培训的总时长是多少？",
            "answer": "2024年在岗安全培训参与人数为730人,共计培训时长3,708小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31170",
            "question": "美新科技的职业健康与安全管理体系认证有哪些？",
            "answer": "美新科技已获得iso 45001职业健康安全管理体系认证和gb/t 33000-2016安全生产标准化认证.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31171",
            "question": "美新科技的安全生产管理委员会由哪些成员组成？",
            "answer": "美新科技的安全生产管理委员会由常务副总经理担任主任,生产运营总监、设备模具总监、安全部主任、人事行政部经理等部门负责人担任副主任,知产法务部主任担任秘书,其余各部门/车间负责人担任成员.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31172",
            "question": "2024年美新科技修订了多少份安全生产管理制度和操作规程？",
            "answer": "\"2024年",
            "document_uuid": "美新科技修订了安全生产管理制度23份",
            "release_status": "安全生产操作规程75份"
        },
        {
            "id": "修订职业健康管理制度13份",
            "question": "职业卫生操作规程4份.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "31173",
            "question": "安全生产管理委员会的主任是谁？",
            "answer": "安全生产管理委员会的主任是常务副总经理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31174",
            "question": "安全生产管理委员会的成员包括哪些？",
            "answer": "安全生产管理委员会的成员包括各部门/车间负责人、安全部主任、安全部专职人员和兼职人员.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31175",
            "question": "美新科技的安全生产方针是什么？",
            "answer": "\"美新科技的安全生产方针是\"\"安全第一",
            "document_uuid": "预防为主",
            "release_status": ""
        },
        {
            "id": "以人为本",
            "question": "全员参与安全发展",
            "answer": "持续改进",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "人人讲安全",
            "question": "个个会应急\"\".\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "31176",
            "question": "2024年美新科技制定了多少项安全生产目标？",
            "answer": "2024年美新科技制定了14项安全生产目标.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31177",
            "question": "2024年美新科技的安全生产目标是否全部达成？",
            "answer": "2024年美新科技的安全生产目标全部达成,完成率100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31178",
            "question": "2024年美新科技的年度工伤事故率是多少？",
            "answer": "\"2024年美新科技的年度工伤事故率是",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "2.35%",
            "question": "低于3%的目标.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "31179",
            "question": "2024年美新科技是否发生了职业病发病情况？",
            "answer": "2024年美新科技没有发生职业病发病情况.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31180",
            "question": "2024年美新科技的安全资金到位率是多少？",
            "answer": "2024年美新科技的安全资金到位率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31181",
            "question": "2024年美新科技的员工安全责任书签订率是多少？",
            "answer": "2024年美新科技的员工安全责任书签订率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31182",
            "question": "2024年美新科技的全员安全培训合格率是多少？",
            "answer": "2024年美新科技的全员安全培训合格率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31183",
            "question": "2024年美新科技的安全防护设备设施完好率是多少？",
            "answer": "2024年美新科技的安全防护设备设施完好率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31184",
            "question": "2024年美新科技的劳动防护设施、器具配备率是多少？",
            "answer": "2024年美新科技的劳动防护设施、器具配备率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31185",
            "question": "2024年美新科技的重大事故隐患整改合格率是多少？",
            "answer": "2024年美新科技的重大事故隐患整改合格率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31186",
            "question": "2024年美新科技的特种设备定期检验率是多少？",
            "answer": "2024年美新科技的特种设备定期检验率是100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31187",
            "question": "美新科技的安全风险防控机制是什么？",
            "answer": "美新科技建立了安全风险分级管控和隐患排查双重预防机制,采用定期检查与专项检查相结合的方式,全面排查生产过程中的安全风险,确保安全生产的持续性和稳定性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31188",
            "question": "2024年美新科技进行了哪些安全培训？",
            "answer": "2024年,美新科技开展了中级消防设施操作员培训240小时,急救员培训296小时,生产安全管理人员和主要负责人初始教育培训40小时,再教育培训96小时,消防安全管理人员和主要负责人再教育培训32小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31189",
            "question": "美新科技的消防队伍是如何设置的？",
            "answer": "\"美新科技设置了消防控制室",
            "document_uuid": "实行24小时全天候值班制度",
            "release_status": "值班消防员全部持证上岗."
        },
        {
            "id": "厂区内配置有消防车",
            "question": "并设立了8人消防队的应急救援力量",
            "answer": "确保遇突发火情时做到1分钟出动、3分钟抵达现场、5分钟扑灭初始火情.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31190",
            "question": "美新科技的安全应急管理措施有哪些？",
            "answer": "\"美新科技严格遵循相关法律法规要求",
            "document_uuid": "更新了<安全生产应急预案>",
            "release_status": "确保消防安全管理有章可循."
        },
        {
            "id": "每月对消防设施进行全面检测",
            "question": "确保疏散通道和安全出口畅通无阻",
            "answer": "及时消除火灾隐患.\"",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31191",
            "question": "2024年美新科技的安全检查频率如何？",
            "answer": "2024年,美新科技的安全部每周进行全厂检查共52次,机械部每月进行设备安全检查12次和用电安全检查46次,主要负责人每月带队进行综合检查12次,合计122次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31192",
            "question": "美新科技的消防值班室有多少名持证上岗的值班人员？",
            "answer": "截至报告期,美新科技的消防值班室共有7名值班人员通过法定消防考试,持证上岗.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31193",
            "question": "美新科技的职业卫生管理委员会是做什么的？",
            "answer": "美新科技的职业卫生管理委员会负责制定全面的职业病危害防治管理制度,并为全体员工建立个人职业卫生档案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31194",
            "question": "美新科技如何保障员工的健康与安全？",
            "answer": "美新科技通过建立职业卫生管理委员会,制定职业病危害防治管理制度,为员工建立个人职业卫生档案,以及每年邀请第三方检测机构进行职业病危害因素监测,来保障员工的健康与安全.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31195",
            "question": "美新科技的职业病危害因素监测是如何进行的？",
            "answer": "美新科技每年邀请有资质的第三方检测机构进行职业病危害因素监测,并将检测报告提交给政府有关部门备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31196",
            "question": "2024年，美新科技进行了多少个岗位的职业危害因素检测？",
            "answer": "2024年,美新科技共计开展了87个不同岗位的职业危害因素检测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31197",
            "question": "美新科技的职业病防治依据哪些法律法规？",
            "answer": "美新科技的职业病防治依据<职业病防治法>和<工作场所职业卫生监督管理规定>等法律法规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31198",
            "question": "美新科技的职业病危害防治管理制度包括哪些内容？",
            "answer": "美新科技的职业病危害防治管理制度包括建立职业卫生管理委员会,制定全面的职业病危害防治管理制度,为员工建立个人职业卫生档案,以及每年进行职业病危害因素监测.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31199",
            "question": "美新科技的职业病危害因素监测报告提交给哪个部门备案？",
            "answer": "美新科技的职业病危害因素监测报告提交给政府有关部门备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31200",
            "question": "美新科技的职业病危害因素监测频率是多少？",
            "answer": "美新科技的职业病危害因素监测频率是每年一次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31201",
            "question": "美新科技的职业病危害因素监测涉及哪些岗位？",
            "answer": "美新科技的职业病危害因素监测涉及87个不同岗位.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31202",
            "question": "美新科技的职业病危害因素监测报告是否公开？",
            "answer": "文本中未提及美新科技的职业病危害因素监测报告是否公开.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31203",
            "question": "美新科技的职业病危害因素监测报告是否需要政府备案？",
            "answer": "是的,美新科技的职业病危害因素监测报告需要提交给政府有关部门备案.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31204",
            "question": "公司识别出的主要职业病危害因素有哪些？",
            "answer": "公司识别出的主要职业病危害因素包括粉尘、噪音和高温.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31205",
            "question": "职业病危害因素涉及哪些岗位？",
            "answer": "职业病危害因素涉及的岗位包括设备模具车间、装配车间、成型车间和备料环保线等.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31206",
            "question": "公司为减少职业病危害因素对员工的影响采取了哪些措施？",
            "answer": "公司为员工配备了完善的劳保用品,在所有工作区域设立了危害因素告示牌,并要求新上岗和调岗的员工签署职业病危害因素告知书.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31207",
            "question": "美新公司为员工提供哪些职业健康检查？",
            "answer": "美新公司为员工提供入职体检和职业健康体检.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31208",
            "question": "入职体检的主要目的是什么？",
            "answer": "入职体检的主要目的是检查员工的身体健康状况是否符合岗位要求,同时识别是否存在潜在的健康风险.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31209",
            "question": "职业健康体检的原则是什么？",
            "answer": "职业健康体检的原则是\"应检尽检\".",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31210",
            "question": "职业健康体检的频率是多少？",
            "answer": "职业健康体检的频率是每年一次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31211",
            "question": "职业健康体检根据什么提供检查？",
            "answer": "职业健康体检根据每个员工的岗位特性提供全面的职业健康检查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31212",
            "question": "职业病危害因素告知书在什么时候签署？",
            "answer": "职业病危害因素告知书在员工新上岗和调岗前签署.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31213",
            "question": "职业健康检查为员工职业发展提供了什么？",
            "answer": "职业健康检查为员工职业发展提供了健康基础.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31214",
            "question": "职业健康检查为公司提供了什么？",
            "answer": "职业健康检查为公司合理安排岗位提供了科学依据.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31215",
            "question": "公司设立了哪些设施来告知员工职业病危害因素？",
            "answer": "公司在所有工作区域设立了危害因素告示牌.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31216",
            "question": "公司为员工配备了哪些用品来减少职业病危害因素的影响？",
            "answer": "公司为员工配备了完善的劳保用品.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31217",
            "question": "职业健康检查涵盖哪些阶段？",
            "answer": "职业健康检查涵盖入职体检和职业健康体检,确保员工在不同阶段都能享受到科学、细致的健康保障.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31218",
            "question": "职业健康检查的目的是什么？",
            "answer": "职业健康检查的目的是确保员工在不同阶段都能享受到科学、细致的健康保障.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31219",
            "question": "2024年美新科技的职业健康体检覆盖率是多少？",
            "answer": "100%",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31220",
            "question": "2024年美新科技是否出现了职业禁忌症和职业病的情况？",
            "answer": "没有出现",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31221",
            "question": "美新科技为新入职员工提供了多少小时的培训？",
            "answer": "24小时",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31222",
            "question": "2024年美新科技共培训了多少名新入职员工？",
            "answer": "273人",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31223",
            "question": "2024年美新科技在岗安全培训共计开展了多少小时？",
            "answer": "3,708小时",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31224",
            "question": "2024年美新科技在岗安全培训共有多少人参与？",
            "answer": "730人",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31225",
            "question": "美新科技为承包商和外部施工人员提供了什么培训？",
            "answer": "专门的安全培训",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31226",
            "question": "美新科技对承包商和外部施工人员的培训内容包括什么？",
            "answer": "施工现场的安全要求和应急措施",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31227",
            "question": "美新科技要求所有承包商和个人必须签署什么文件？",
            "answer": "安全协议",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31228",
            "question": "美新科技的安全协议目的是什么？",
            "answer": "确保其严格遵守公司的安全管理规定",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31229",
            "question": "美新科技建立了什么样的培训体系？",
            "answer": "系统化的培训体系",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31230",
            "question": "美新科技的培训体系确保员工在不同阶段掌握什么？",
            "answer": "必要的安全知识和技能",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31231",
            "question": "美新科技依托哪些培训为员工提供全面的生产安全培训和职业健康安全培训？",
            "answer": "内部入职培训和在岗培训",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31232",
            "question": "美新科技的安全理念是否仅限于自身员工？",
            "answer": "不,还向外部进行传导",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31233",
            "question": "美新科技的安全理念向哪些外部人员传导？",
            "answer": "承包商和外部施工人员",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31234",
            "question": "美新科技2024年共开展了多少次应急演练？",
            "answer": "美新科技2024年共开展了14次应急演练.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31235",
            "question": "美新科技2024年应急演练的参与人数是多少？",
            "answer": "美新科技2024年应急演练的参与人数共计804人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31236",
            "question": "美新科技2024年开展了哪些类型的应急演练？",
            "answer": "美新科技2024年开展了专项演练、应急疏散和综合演练三种类型的应急演练.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31237",
            "question": "美新科技2024年开展了几次综合演练？",
            "answer": "美新科技2024年开展了2次综合演练.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31238",
            "question": "美新科技2024年开展了几次疏散演练？",
            "answer": "美新科技2024年开展了2次疏散演练.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31239",
            "question": "美新科技2024年开展了几次专项演练？",
            "answer": "美新科技2024年开展了10次专项演练.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31240",
            "question": "美新科技2024年哪次应急演练的参与人数最多？",
            "answer": "\"美新科技2024年安全生产综合应急演练",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "二)的参与人数最多",
            "question": "为241人.\"",
            "answer": "cd9b7bc224a111f080617233a72c882c",
            "document_uuid": "qa_await",
            "release_status": ""
        },
        {
            "id": "31241",
            "question": "美新科技2024年哪次应急演练的参与人数最少？",
            "answer": "美新科技2024年粉尘爆炸事故应急演练的参与人数最少,为16人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31242",
            "question": "美新科技2024年应急演练的目的为何？",
            "answer": "美新科技2024年应急演练的目的是提升员工应对突发事件的能力,确保在突发事件发生时能够迅速、有序地采取应对措施.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31243",
            "question": "美新科技2024年应急演练项目中，火灾事故应急演练共进行了几次？",
            "answer": "美新科技2024年应急演练项目中,火灾事故应急演练共进行了2次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31244",
            "question": "美新科技2024年应急演练项目中，应急疏散演练的参与人数是多少？",
            "answer": "美新科技2024年应急演练项目中,应急疏散演练的参与人数共计152人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31245",
            "question": "美新科技2024年的安全生产目标是什么？",
            "answer": "美新科技2024年的安全生产目标包括零重大设备事故、零重大责任事故、零职业病员工、安全培训全覆盖、安全隐患整改全覆盖、特种作业员工持证上岗全覆盖等共计15项总体目标.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31246",
            "question": "2024年美新科技及分公司、子公司是否发生重大安全事故？",
            "answer": "截至2024年末,美新科技及分公司、子公司未发生重大安全事故.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31247",
            "question": "2024年美新科技的职业健康与安全生产培训人数是多少？",
            "answer": "2024年美新科技的职业健康与安全生产培训人数为9137人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31248",
            "question": "2024年美新科技的职业健康与安全生产培训总时长是多少？",
            "answer": "2024年美新科技的职业健康与安全生产培训总时长为832小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31249",
            "question": "2024年美新科技的生产安全管理员培训人数是多少？",
            "answer": "2024年美新科技的生产安全管理员培训人数为5人.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31250",
            "question": "2024年美新科技的生产安全管理员培训总时长是多少？",
            "answer": "2024年美新科技的生产安全管理员培训总时长为136小时.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31251",
            "question": "2024年美新科技的安全生产演练总次数是多少？",
            "answer": "2024年美新科技的安全生产演练总次数为14次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31252",
            "question": "2024年美新科技的专项演练次数是多少？",
            "answer": "2024年美新科技的专项演练次数为10次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31253",
            "question": "2024年美新科技的综合演练次数是多少？",
            "answer": "2024年美新科技的综合演练次数为2次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31254",
            "question": "2024年美新科技的应急疏散演练次数是多少？",
            "answer": "2024年美新科技的应急疏散演练次数为2次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31255",
            "question": "2024年美新科技的安全生产演练合计参与总人次是多少？",
            "answer": "2024年美新科技的安全生产演练合计参与总人次为804人次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31256",
            "question": "2024年美新科技的安全生产投入总金额是多少？",
            "answer": "2024年美新科技的安全生产投入总金额为417.89万元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31257",
            "question": "2024年美新科技的风险识别与隐患排查总次数是多少？",
            "answer": "2024年美新科技的风险识别与隐患排查总次数为770次.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31258",
            "question": "2024年美新科技识别的安全生产相关风险及隐患数量是多少？",
            "answer": "2024年美新科技识别的安全生产相关风险及隐患数量为771个.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31259",
            "question": "2024年美新科技的安全生产相关风险与隐患完成整改比例是多少？",
            "answer": "2024年美新科技的安全生产相关风险与隐患完成整改比例为100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31260",
            "question": "美新科技2024年的安全生产目标是否全部达成？",
            "answer": "截至2024年末,美新科技设定的安全生产目标全部达成.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31261",
            "question": "美新科技2024年的安全生产目标是否包括零职业病员工？",
            "answer": "是的,美新科技2024年的安全生产目标包括零职业病员工.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31262",
            "question": "美新科技2024年的安全生产目标是否包括安全培训全覆盖？",
            "answer": "是的,美新科技2024年的安全生产目标包括安全培训全覆盖.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31263",
            "question": "美新科技2024年的安全生产目标是否包括安全隐患整改全覆盖？",
            "answer": "是的,美新科技2024年的安全生产目标包括安全隐患整改全覆盖.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31264",
            "question": "美新科技2024年的安全生产目标是否包括特种作业员工持证上岗全覆盖？",
            "answer": "是的,美新科技2024年的安全生产目标包括特种作业员工持证上岗全覆盖.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31265",
            "question": "2024年美新科技的安全生产演练中，专项演练占总演练次数的比例是多少？",
            "answer": "2024年美新科技的专项演练占总演练次数的比例为71.43%(10次/14次).",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31266",
            "question": "2024年美新科技的安全生产演练中，综合演练占总演练次数的比例是多少？",
            "answer": "2024年美新科技的综合演练占总演练次数的比例为14.29%(2次/14次).",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31267",
            "question": "2024年美新科技的安全生产演练中，应急疏散演练占总演练次数的比例是多少？",
            "answer": "2024年美新科技的应急疏散演练占总演练次数的比例为14.29%(2次/14次).",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31268",
            "question": "2024年美新科技的安全生产投入总金额占风险识别与隐患排查总次数的比例是多少？",
            "answer": "2024年美新科技的安全生产投入总金额占风险识别与隐患排查总次数的比例为0.5425万元/次(417.89万元/770次).",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31269",
            "question": "2024年美新科技的安全生产演练合计参与总人次占风险识别与隐患排查总次数的比例是多少？",
            "answer": "\"2024年美新科技的安全生产演练合计参与总人次占风险识别与隐患排查总次数的比例为",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "1.0441人次/次(804人次/770次).\"",
            "question": "cd9b7bc224a111f080617233a72c882c",
            "answer": "qa_await",
            "document_uuid": "",
            "release_status": ""
        },
        {
            "id": "31270",
            "question": "2024年美新科技的安全生产相关风险与隐患完成整改比例是否达到100%？",
            "answer": "是的,2024年美新科技的安全生产相关风险与隐患完成整改比例达到了100%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31271",
            "question": "2024年美新科技的安全生产相关风险与隐患完成整改比例是否达到90%？",
            "answer": "是的,2024年美新科技的安全生产相关风险与隐患完成整改比例达到了100%,远超90%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31272",
            "question": "2024年美新科技的安全生产相关风险与隐患完成整改比例是否达到80%？",
            "answer": "是的,2022年美新科技的安全生产相关风险与隐患完成整改比例达到了100%,远超80%.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31273",
            "question": "美新科技在社会贡献方面做了哪些工作？",
            "answer": "\"美新科技通过捐资、捐物、帮扶采购等方式参与社会慈善和乡村振兴",
            "document_uuid": "如参与广东省政府的\"\"百县千镇万村高质量发展工程\"\"",
            "release_status": "助力乡村规划、产业发展和基础设施建设.\"",
            "": "qa_await"
        },
        {
            "id": "31274",
            "question": "美新科技在2024年参与了哪些具体的乡村振兴行动？",
            "answer": "\"美新科技参与了广东省政府的\"\"千企帮千镇、万企兴万村\"\"行动",
            "document_uuid": "通过捐资、捐物、帮扶采购等方式与各类企业携手",
            "release_status": "共同助力乡村规划、产业发展和基础设施建设.\"",
            "": "qa_await"
        },
        {
            "id": "31275",
            "question": "美新科技在公益方面做了哪些努力？",
            "answer": "美新科技开展了包括公益助跑、环保公益捐赠、养老社区改善等在内的一系列社会公益活动,共计捐赠善款近70万元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31276",
            "question": "美新科技响应了哪些政府政策？",
            "answer": "美新科技响应了广东省政府的\"\"百县千镇万村高质量发展工程\"",
            "document_uuid": "积极参与城乡区域协调发展的战略部署.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "31277",
            "question": "美新科技在乡村振兴方面投入了多少资金？",
            "answer": "美新科技在乡村振兴方面共计捐赠善款近70万元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31278",
            "question": "美新科技如何参与乡村规划和基础设施建设？",
            "answer": "美新科技通过捐资、捐物、帮扶采购等方式与各类企业携手,共同助力乡村规划和基础设施建设.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31279",
            "question": "美新科技在环保方面做了哪些公益活动？",
            "answer": "美新科技开展了环保公益捐赠等公益活动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31280",
            "question": "美新科技在养老社区方面做了哪些工作？",
            "answer": "美新科技开展了养老社区改善等公益活动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31281",
            "question": "美新科技在社会贡献方面有哪些具体项目？",
            "answer": "美新科技参与了公益助跑、环保公益捐赠、养老社区改善等项目.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31282",
            "question": "美新科技在社会贡献方面有哪些具体行动？",
            "answer": "\"美新科技通过捐资、捐物、帮扶采购等方式参与社会慈善和乡村振兴",
            "document_uuid": "如参与广东省政府的\"\"千企帮千镇、万企兴万村\"\"行动.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "31283",
            "question": "美新科技在社会贡献方面有哪些具体成果？",
            "answer": "美新科技共计捐赠善款近70万元,参与了乡村规划、产业发展和基础设施建设等项目.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31284",
            "question": "美新科技在社会贡献方面有哪些具体措施？",
            "answer": "\"美新科技通过捐资、捐物、帮扶采购等方式参与社会慈善和乡村振兴",
            "document_uuid": "如参与广东省政府的\"\"千企帮千镇、万企兴万村\"\"行动.\"",
            "release_status": "cd9b7bc224a111f080617233a72c882c"
        },
        {
            "id": "31285",
            "question": "美新科技在社会贡献方面有哪些具体活动？",
            "answer": "美新科技开展了公益助跑、环保公益捐赠、养老社区改善等公益活动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31286",
            "question": "美新科技在社会贡献方面有哪些具体捐赠？",
            "answer": "美新科技共计捐赠善款近70万元.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31287",
            "question": "美新科技在社会贡献方面有哪些具体帮扶？",
            "answer": "美新科技通过捐资、捐物、帮扶采购等方式与各类企业携手,共同助力乡村规划、产业发展和基础设施建设.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31288",
            "question": "美新科技在社会贡献方面有哪些具体合作？",
            "answer": "美新科技通过捐资、捐物、帮扶采购等方式与各类企业携手,共同助力乡村规划、产业发展和基础设施建设.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31289",
            "question": "美新科技在商业道德和公司治理方面有何举措？",
            "answer": "美新科技高度重视商业道德和公司治理,致力于构建透明、规范的经营环境,坚决反对任何形式的贪污、腐败和不正当竞争行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31290",
            "question": "美新科技如何确保经营活动的合法合规？",
            "answer": "美新科技通过完善的风险管理机制和规范的内部治理结构,确保经营活动的合法合规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31291",
            "question": "美新科技在与利益相关方的沟通与协作方面有何做法？",
            "answer": "美新科技注重与利益相关方的沟通与协作,积极参与行业对话和社会责任实践,推动企业与社会的和谐发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31292",
            "question": "尽职调查遵循的原则是什么？",
            "answer": "尽职调查遵循的原则是客观.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31293",
            "question": "美新科技如何推动企业与社会的和谐发展？",
            "answer": "美新科技通过积极参与行业对话和社会责任实践,推动企业与社会的和谐发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31294",
            "question": "美新科技的治理篇主要强调什么？",
            "answer": "美新科技的治理篇主要强调构建透明、规范的经营环境,反对任何形式的贪污、腐败和不正当竞争行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31295",
            "question": "美新科技的内部治理结构有何特点？",
            "answer": "美新科技的内部治理结构特点是规范,通过完善的风险管理机制确保经营活动的合法合规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31296",
            "question": "美新科技如何与利益相关方进行沟通？",
            "answer": "美新科技注重与利益相关方的沟通与协作,积极参与行业对话和社会责任实践.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31297",
            "question": "美新科技的治理篇中提到了哪些行为是坚决反对的？",
            "answer": "美新科技坚决反对任何形式的贪污、腐败和不正当竞争行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31298",
            "question": "美新科技的治理篇中提到了哪些机制来确保经营活动的合法合规？",
            "answer": "美新科技通过完善的风险管理机制和规范的内部治理结构来确保经营活动的合法合规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31299",
            "question": "美新科技的治理篇中提到了哪些社会责任实践？",
            "answer": "美新科技积极参与行业对话和社会责任实践,推动企业与社会的和谐发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31300",
            "question": "美新科技的治理篇中提到了哪些方面来构建透明的经营环境？",
            "answer": "美新科技通过完善的风险管理机制和规范的内部治理结构来构建透明的经营环境.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31301",
            "question": "美新科技的治理篇中提到了哪些方面来确保经营活动的合法合规？",
            "answer": "美新科技通过完善的风险管理机制和规范的内部治理结构来确保经营活动的合法合规.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31302",
            "question": "美新科技如何重视与利益相关方的沟通？",
            "answer": "美新科技通过定期的调研活动和投资者交流会议,积极回应市场关切,展示公司的发展战略和运营状况.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31303",
            "question": "美新科技与利益相关方的沟通目的是什么？",
            "answer": "旨在增进彼此之间的理解与信任,推动企业稳健发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31304",
            "question": "美新科技建立了怎样的管理框架来沟通利益相关方？",
            "answer": "美新科技建立了系统化的管理框架,形成了全面立体的沟通体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31305",
            "question": "美新科技的治理理念是什么？",
            "answer": "美新科技秉持开放协同的治理理念.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31306",
            "question": "美新科技如何构建互动机制？",
            "answer": "美新科技构建了多维度、深层次的互动机制,通过持续的信息共享机制与各利益相关方保持高效联动.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31307",
            "question": "美新科技如何响应利益相关方的诉求？",
            "answer": "美新科技建立了动态化的诉求响应体系,采取定期沟通会议、专项调研与业务协作相结合的方式.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31308",
            "question": "美新科技如何确保各方诉求融入公司决策体系？",
            "answer": "通过定期沟通会议、专项调研与业务协作相结合的方式,确保各方诉求能够及时有效地融入公司决策体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31309",
            "question": "美新科技如何实现多方利益的均衡与共赢？",
            "answer": "通过确保各方诉求能够及时有效地融入公司决策体系,从而实现多方利益的均衡与共赢.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31310",
            "question": "美新科技围绕哪些议题展开深入沟通？",
            "answer": "美新科技围绕战略规划、项目执行等多维度议题展开深入沟通.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31311",
            "question": "美新科技如何制定沟通策略？",
            "answer": "根据不同利益相关方的特征制定差异化的沟通策略.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31312",
            "question": "美新科技如何调整沟通深度与呈现形式？",
            "answer": "动态调整沟通深度与呈现形式,以实现精准化信息传递.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31313",
            "question": "美新科技如何提升利益相关方参与公司治理的深度？",
            "answer": "通过构建全方位的沟通机制,有效提升了利益相关方参与公司治理的深度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31314",
            "question": "美新科技如何促进形成可持续发展的合作生态？",
            "answer": "通过构建全方位的沟通机制,促进形成可持续发展的合作生态.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31315",
            "question": "美新科技如何与供应商沟通？",
            "answer": "采取定期沟通会议、专项调研与业务协作相结合的方式,确保供应商的诉求能够及时有效地融入公司决策体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31316",
            "question": "美新科技如何与客户沟通？",
            "answer": "采取定期沟通会议、专项调研与业务协作相结合的方式,确保客户的诉求能够及时有效地融入公司决策体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31317",
            "question": "美新科技如何与投资者沟通？",
            "answer": "采取定期沟通会议、专项调研与业务协作相结合的方式,确保投资者的诉求能够及时有效地融入公司决策体系.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31318",
            "question": "美新科技如何展示公司的发展战略和运营状况？",
            "answer": "通过定期的调研活动和投资者交流会议,展示公司的发展战略和运营状况.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31319",
            "question": "美新科技如何回应市场关切？",
            "answer": "通过定期的调研活动和投资者交流会议,积极回应市场关切.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31320",
            "question": "美新科技如何增进与利益相关方之间的理解与信任？",
            "answer": "通过定期的调研活动和投资者交流会议,增进与利益相关方之间的理解与信任.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31321",
            "question": "美新科技如何推动企业稳健发展？",
            "answer": "通过定期的调研活动和投资者交流会议,积极回应市场关切,展示公司的发展战略和运营状况,增进与利益相关方之间的理解与信任,推动企业稳健发展.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31322",
            "question": "美新科技如何实现精准化信息传递？",
            "answer": "通过动态调整沟通深度与呈现形式,实现精准化信息传递.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31323",
            "question": "公司董事会的主要职责是什么？",
            "answer": "公司董事会积极履行治理责任,制定并实施全面的反贪腐计划,确保相关制度的严格执行,并对高风险业务领域进行持续监督与合规审查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31324",
            "question": "董事会如何评估反腐败管理体系的有效性？",
            "answer": "董事会定期评估反腐败管理体系的有效性,推动管理层落实廉洁经营责任,同时加强内部沟通与培训,提升全员合规意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31325",
            "question": "公司如何确保在全球运营中的公正性和透明度？",
            "answer": "公司通过加强内部沟通与培训,提升全员合规意识,确保在全球运营中的公正性和透明度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31326",
            "question": "美新科技建立了哪些举报渠道？",
            "answer": "美新科技建立了<员工意见、建议、申诉及反馈管理程序>,为员工提供安全、透明的举报渠道,包括通过员工意见箱提交书面举报内容,由专人每天在工作日结束前统一收集.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31327",
            "question": "举报渠道的目的是什么？",
            "answer": "举报渠道的目的是确保任何涉及贪污、贿赂、利益输送等不当行为能够被及时发现和处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31328",
            "question": "公司如何推动廉洁经营责任的落实？",
            "answer": "公司通过董事会定期评估反腐败管理体系的有效性,推动管理层落实廉洁经营责任.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31329",
            "question": "公司如何提升全员的合规意识？",
            "answer": "公司通过加强内部沟通与培训,提升全员的合规意识.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31330",
            "question": "公司如何确保相关制度的严格执行？",
            "answer": "公司通过制定并实施全面的反贪腐计划,确保相关制度的严格执行.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31331",
            "question": "公司如何对高风险业务领域进行监督？",
            "answer": "公司对高风险业务领域进行持续监督与合规审查.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31332",
            "question": "公司如何确保员工举报的及时处理？",
            "answer": "公司设立了多种举报方式,包括通过员工意见箱提交书面举报内容,由专人每天在工作日结束前统一收集,确保员工举报的及时处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31333",
            "question": "公司如何确保员工举报的安全性？",
            "answer": "公司建立了<员工意见、建议、申诉及反馈管理程序>,为员工提供安全、透明的举报渠道,确保员工举报的安全性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31334",
            "question": "公司如何确保员工举报的透明性？",
            "answer": "公司建立了<员工意见、建议、申诉及反馈管理程序>,为员工提供安全、透明的举报渠道,确保员工举报的透明性.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31335",
            "question": "公司如何确保员工举报的有效性？",
            "answer": "公司通过设立多种举报方式,确保员工举报的有效性,包括通过员工意见箱提交书面举报内容,由专人每天在工作日结束前统一收集.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31336",
            "question": "公司如何确保员工举报的及时发现？",
            "answer": "公司通过设立多种举报方式,确保员工举报的及时发现,包括通过员工意见箱提交书面举报内容,由专人每天在工作日结束前统一收集.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31337",
            "question": "公司如何确保员工举报的及时反馈？",
            "answer": "公司通过设立多种举报方式,确保员工举报的及时反馈,包括通过员工意见箱提交书面举报内容,由专人每天在工作日结束前统一收集.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31338",
            "question": "如何举报员工问题？",
            "answer": "可以通过拨打员工投诉热线,或直接向部门或区域负责人进行口头投诉.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31339",
            "question": "举报信息如何处理？",
            "answer": "举报信息将由专人每日在固定时段接听并详细记录,所有举报内容将由行政部负责接收、分类并整理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31340",
            "question": "举报信息是否保密？",
            "answer": "所有举报信息均受到严格保密,公司承诺保护举报人身份,杜绝任何形式的报复或不公正待遇.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31341",
            "question": "举报渠道有哪些？",
            "answer": "举报/反馈渠道包括员工意见箱、投诉热线、口头投诉.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31342",
            "question": "举报信息如何管理？",
            "answer": "所有举报信息由专人负责汇总、登记,并纳入<员工投诉记录表>,确保举报事项得到有效跟踪和及时处置.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31343",
            "question": "举报内容审查后如何处理？",
            "answer": "举报内容经审查后,公司将根据调查结果采取相应措施,包括内部整改、纪律处分,必要时移交执法机构处理.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31344",
            "question": "公司如何优化举报管理体系？",
            "answer": "公司定期审查和优化举报管理体系,以提升廉洁管理的透明度和执行力,构建风清气正的企业文化.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31345",
            "question": "美新科技如何确保公平竞争？",
            "answer": "美新科技制定了<公平竞争控制程序>,以确保企业在市场竞争中的合规性和透明度.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31346",
            "question": "美新科技如何避免恶性竞争？",
            "answer": "公司在与经销商及其他合作伙伴签订合作协议时,明确纳入反不正当竞争条款,确保合作方遵循公平竞争原则,避免恶性竞争、虚假宣传或恶意诋毁.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31347",
            "question": "美新科技如何确保品牌形象的统一性？",
            "answer": "公司在代理协议中明确要求经销商在授权范围内正确使用商标,并在规定地域内销售产品,不得经营未经授权的其他商品.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31348",
            "question": "2024年美新科技是否因不正当竞争行为导致诉讼？",
            "answer": "2024年,美新科技及下属产业板块未因不正当竞争行为导致诉讼或重大行政处罚.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31349",
            "question": "2024年美新科技是否发生侵犯知识产权的行为？",
            "answer": "2024年,美新科技及下属产业板块没有发生侵犯知识产权的行为.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31350",
            "question": "报告中提到的环境议题有哪些？",
            "answer": "报告中提到的环境议题包括应对气候变化、污染物排放、废弃物处理、生态系统和生物多样性保护、环境合规管理、能源利用、水资源利用和循环经济.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31351",
            "question": "社会议题中提到了哪些内容？",
            "answer": "社会议题中提到了乡村振兴、社会贡献、创新驱动、供应链安全、产品和服务安全与质量、数据安全与客户隐私保护以及员工.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31352",
            "question": "报告中是否有提到科技伦理？",
            "answer": "报告中提到科技伦理,但标注为不适用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31353",
            "question": "报告中关于平等对待中小企业的议题是什么状态？",
            "answer": "报告中关于平等对待中小企业的议题标注为不适用.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31354",
            "question": "报告中提到了哪些治理相关的议题？",
            "answer": "报告中提到的治理相关议题包括尽职调查、利益相关方沟通、反商业贿赂及反贪污、反不正当竞争.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31355",
            "question": "报告中关于可持续发展的附录引用了哪个指引？",
            "answer": "报告中关于可持续发展的附录引用了<深圳证券交易所上市公司自律监管指引第17号⸺可持续发展报告(试行)>.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31356",
            "question": "读者可以通过哪些方式反馈对《美新科技股份有限公司2024年可持续发展报告》的意见？",
            "answer": "读者可以通过邮寄或扫描后发送电子邮件的方式将填好的问卷反馈给美新科技.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31357",
            "question": "美新科技的地址是什么？",
            "answer": "广东省惠州市惠东县大岭街道十二托乌塘地段.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31358",
            "question": "美新科技的联系电话是什么？",
            "answer": "0752-6531633.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31359",
            "question": "读者对报告的可读性评价分为哪几个等级？",
            "answer": "读者对报告的可读性评价分为3分(较好)、2分(一般)和1分(极差)三个等级.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31360",
            "question": "读者反馈意见时需要填写哪些选择性问题？",
            "answer": "读者需要选择其工作单位属于美新科技的哪一类,包括政府/监管机构、股东/投资者、行业研究员、客户供应商/承包商、员工、社区、非盈利组织或其他(请说明).",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31361",
            "question": "美新科技希望读者对报告的哪些方面提出意见？",
            "answer": "美新科技希望读者对报告的综合评价,包括可读性、表达方式、设计美观度、引人入胜程度以及是否容易找到所需信息等方面提出意见.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31362",
            "question": "报告中是否包含了您所关注的所有信息？",
            "answer": "根据调查,53%的受访者表示报告中包含了他们所关注的所有信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        },
        {
            "id": "31363",
            "question": "有多少比例的受访者认为报告中没有体现他们所关注的信息？",
            "answer": "调查结果显示,47%的受访者认为报告中没有体现他们所关注的信息.",
            "document_uuid": "cd9b7bc224a111f080617233a72c882c",
            "release_status": "qa_await"
        }
    ]


    qa_release_valiate(docs)
