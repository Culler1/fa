import os, sys, requests, random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup as Soup

def getR16():
    return ''.join(random.choice('0123456789') for i in range(16))

def getList(murlpart):
    r16 = getR16()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://go.boarddocs.com/'+murlpart+'/Board.nsf/Public',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://go.boarddocs.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    data = {
        'status': 'active',
        'book': 'Policy Manual',
        'current_committee_id': '',
    }

    response = requests.post(
        'https://go.boarddocs.com/'+murlpart+'/Board.nsf/BD-GetPolicies?open&0.'+r16,
        headers=headers,
        data=data,
    )

    soup = Soup(response.content, 'lxml')
    plist = []
    for a in soup.find_all('a'):
        uid = a.get('unique')
        if uid:
            #print(a)
            try:
                a.find('div', {'class':'icons'}).decompose()
            except:
                pass
            adivs = a.find_all('div')
            name = adivs[0].get_text().strip()+': '+adivs[1].get_text().strip()
            print(uid, name)
            plist.append({'uid':uid, 'name':name})

    return plist
    #print(response.content)


def getDetail(murlpart, uid):
    r16 = getR16()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://go.boarddocs.com/'+murlpart+'/Board.nsf/goto',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://go.boarddocs.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    data = {
        'id': uid,
        'current_committee_id': '',
    }

    response = requests.post(
        'https://go.boarddocs.com/'+murlpart+'/Board.nsf/BD-GetPolicyItem?open&0.'+r16,
        headers=headers,
        data=data,
    )

    print(response.content)

##############################################################
########################## TRIGGERS ##########################
##############################################################


mup = 'pa/clea'

policy_menu_list = getList(mup)
# policy_menu_list = [{'uid': 'A2TPD8641494', 'name': '000: Board Policy/Procedure/Administrative Regulations'}, {'uid': 'A2TPDA64164F', 'name': '001: Name And Classification'}, {'uid': 'A2TPDB64178C', 'name': '002: Authority And Powers'}, {'uid': 'A2TPDC6418BE', 'name': '003: Functions'}, {'uid': 'A2TPDE641AF7', 'name': '004: Membership'}, {'uid': 'A2TPDM642327', 'name': '005: Organization'}, {'uid': 'A2TPDQ642739', 'name': '006: Meetings'}, {'uid': 'A2TPEE64404E', 'name': '006.1: Use Of Electronic Communication Equipment'}, {'uid': 'A2TPEF644179', 'name': '007: Distribution'}, {'uid': 'A2TPEH64441F', 'name': '008: Organization Chart'}, {'uid': 'A2TPEJ644561', 'name': '011: Board Governance Standards/Code Of Conduct'}, {'uid': 'A2TPEN6449BE', 'name': '100: Strategic Plan'}, {'uid': 'A2TPEQ644BD8', 'name': '101: Mission Statement/Vision Statement'}, {'uid': 'A2TPER644CA6', 'name': '102: Academic Standards'}, {'uid': 'A2TPES644ED7', 'name': '103: Nondiscrimination In School And Classroom Practices'}, {'uid': 'A2TPEX6454A9', 'name': '103.1: Nondiscrimination – Qualified Students With Disabilities'}, {'uid': 'A2TPF5645B75', 'name': '104: Nondiscrimination In Employment And Contract Practices'}, {'uid': 'A2TPF8645F22', 'name': '105: Curriculum Development'}, {'uid': 'A2TPFB6462BF', 'name': '105.1: Curriculum Review By Parents/Guardians And Students'}, {'uid': 'A2TPFD6464AE', 'name': '105.2: Exemption From Instruction'}, {'uid': 'A2TPFE6466A0', 'name': '106: Guides For Planned Instruction'}, {'uid': 'A2TPFG646863', 'name': '107: Adoption Of Planned Instruction'}, {'uid': 'A2TPFJ646A9C', 'name': '108: Adoption Of Textbooks'}, {'uid': 'A2TPFK646B70', 'name': '109: Resource Materials'}, {'uid': 'A2TPFL646C35', 'name': '110: Instructional Supplies'}, {'uid': 'A2TPFM646D01', 'name': '111: Lesson Plans'}, {'uid': 'A2TPFN646DE6', 'name': '112: Guidance Counseling'}, {'uid': 'A2TPFP64700A', 'name': '113: Special Education'}, {'uid': 'A2TPFU647609', 'name': '113.1: Discipline Of Students With Disabilities'}, {'uid': 'A2TPFY647BA4', 'name': '113.2: Behavior Support'}, {'uid': 'A2TPG464806A', 'name': '113.3: Screening And Evaluations For Students With Disabilities'}, {'uid': 'BWXT3U757305', 'name': '113.4: Confidentiality of Special Education Student Information'}, {'uid': 'A2TPGA648693', 'name': '114: Gifted Education'}, {'uid': 'A2TPGD6489F4', 'name': '115: Career And Technical Education'}, {'uid': 'A2TPGE648AFC', 'name': '116: Tutoring'}, {'uid': 'A2TPGF648C52', 'name': '117: Homebound Instruction'}, {'uid': 'A2TPGG648E74', 'name': '118: Independent Study'}, {'uid': 'A2TPGH648F48', 'name': '119: Current Events'}, {'uid': 'A2TPGK64916D', 'name': '121: Field Trips'}, {'uid': 'A2TPGN649573', 'name': '122: Extracurricular Activities'}, {'uid': 'AGTQJN66AF25', 'name': '123: Copy of Interscholastic Athletics'}, {'uid': 'A2TPGT649B38', 'name': '124: Alternative Instruction Courses'}, {'uid': 'A2TPGU649C43', 'name': '125: Adult Education'}, {'uid': 'A2TPGV649D3E', 'name': '126: Class Size'}, {'uid': 'A2TPGW649E3D', 'name': '127: Assessments'}, {'uid': 'A2TPGX64A013', 'name': '130: Homework'}, {'uid': 'A2TPH264A29E', 'name': '137: Home Education Programs'}, {'uid': 'A2TPH364A4BB', 'name': '137.1: Extracurricular Participation By Home Education Students'}, {'uid': 'A2TPH564A633', 'name': '138: Language Instruction Educational Program for English Learners'}, {'uid': 'A2TPH764A8DA', 'name': '140: Charter Schools'}, {'uid': 'A2TPHC64AE4A', 'name': '140.1: Extracurricular Participation By Charter/Cyber Charter Students'}, {'uid': 'A2TPHD64AFCE', 'name': '141: Cyber Services Program'}, {'uid': 'A2TPHG64B3A8', 'name': '142: Migrant Students'}, {'uid': 'A2TPHJ64B5BB', 'name': '143: Standards For Persistently Dangerous Schools'}, {'uid': 'A2TPHN64BA8B', 'name': '144: Standards For Victims Of Violent Crimes'}, {'uid': 'A2TPHQ64BC74', 'name': '146: Student Services'}, {'uid': 'A2TPHS64BEE4', 'name': '200: Enrollment Of Students'}, {'uid': 'A2TPHT64C0A3', 'name': '201: Admission Of Students'}, {'uid': 'A2TPHV64C29B', 'name': '202: Eligibility Of Nonresident Students'}, {'uid': 'A2TPHX64C4DF', 'name': '203: Immunizations And Communicable Diseases'}, {'uid': 'A2TPHZ64C7A2', 'name': '203.1: HIV Infection'}, {'uid': 'A2TPJ464CB71', 'name': '204: Attendance'}, {'uid': 'A2TPJD64D52F', 'name': '206: Assignment Within District'}, {'uid': 'A2TPJE64D705', 'name': '207: Confidential Communications Of Students'}, {'uid': 'A2TPJF64D7C6', 'name': '208: Withdrawal From School'}, {'uid': 'A2TPJH64D9F5', 'name': '209: Health Examinations/Screenings'}, {'uid': 'AGSR9V6CDF3E', 'name': '210: Use of Medications'}, {'uid': 'AGSRFK6DCA2B', 'name': '210 AR: Use of Medications Administrative Regulations'}, {'uid': 'AGSRWT6FD89A', 'name': '210.1: Possession/ Use of Asthma Inhalers/ Epinephrine Auto-Injectors'}, {'uid': 'A2TPJU64E768', 'name': '216.1: Supplemental Discipline Records'}, {'uid': 'A2TPJV64E8A1', 'name': '217: Graduation Requirements'}, {'uid': 'A2TPJY64EBE5', 'name': '218: Student Discipline'}, {'uid': 'A2TPK364EF09', 'name': '218.1: Weapons'}, {'uid': 'A2TPK564F1B8', 'name': '218.2: Terroristic Threats/Acts'}, {'uid': 'A2TPK664F324', 'name': '218.3: Violent And Dangerous Behavior'}, {'uid': 'A2TPK764F435', 'name': '218.4: Conduct Toward Staff Members And Adults'}, {'uid': 'A2TPK864F517', 'name': '219: Student Complaint Process'}, {'uid': 'BH6NXT621D0A', 'name': '220.1: Student Walkouts/ Demonstration/ Related School Activities'}, {'uid': 'A2TPKD64FA83', 'name': '221: Dress And Grooming'}, {'uid': 'A2TPKE64FB53', 'name': '222: Tobacco Use'}, {'uid': 'A2TPKJ650005', 'name': '225: Relations With Law Enforcement Agencies'}, {'uid': 'A2TPKK650120', 'name': '226: Searches'}, {'uid': 'A2TPKL6502B4', 'name': '227: Controlled Substances/Paraphernalia'}, {'uid': 'BPALZY57DC9F', 'name': '233: Suspension and Expulsion'}, {'uid': 'A2TPL7651948', 'name': '236: Student Assistance Program'}, {'uid': 'A2TPLA651CD7', 'name': '238: Student Custody'}, {'uid': 'BFEJUC4E8714', 'name': '246: School Wellness'}, {'uid': 'AGSRTC6F80B2', 'name': '247: Hazing'}, {'uid': 'A2TPLK6527DF', 'name': '248: Unlawful Harassment'}, {'uid': 'C43LQ2578D5F', 'name': '249: Bullying/Cyberbullying'}, {'uid': 'AGWPFQ644FEA', 'name': '251: Homeless Students'}, {'uid': 'B8FTJ569A662', 'name': '252: Dating Violence'}, {'uid': 'A2TPM6653DA6', 'name': '304: Employment Of District Staff'}, {'uid': 'A2TPMA6542F5', 'name': '306: Employment Of Summer School Staff'}, {'uid': 'A2TPMC65443D', 'name': '307: Student Teachers/Interns'}, {'uid': 'A2TPMM654F3A', 'name': '312: Evaluation Of Superintendent'}, {'uid': 'A2TPMQ655282', 'name': '314: Physical Examination'}, {'uid': 'A2TPMW65599C', 'name': '317: Conduct/Disciplinary Procedures'}, {'uid': 'B8FTJ969A668', 'name': '317.1: Employee Misconduct'}, {'uid': 'A2TPMZ655D5A', 'name': '319: Conflict of Interest - Prohibited Activities'}, {'uid': 'A2TPN6656297', 'name': '323: Tobacco Use'}, {'uid': 'A2TPN96566AC', 'name': '325: Dress And Grooming'}, {'uid': 'A2TPP3658493', 'name': '340: Responsibility For Student Welfare'}, {'uid': 'A2TPP9658BC8', 'name': '348: Unlawful Harassment'}, {'uid': 'A2TPNH65701A', 'name': '431: Job Related Expenses'}, {'uid': 'A2TPPF659392', 'name': '448: Unlawful Harassment'}, {'uid': 'A2TPPL6599B4', 'name': '548: Unlawful Harassment'}, {'uid': 'AJDVVS71D5F2', 'name': '610.1: Procurement Plan'}, {'uid': 'AJDVTY719994', 'name': '610.2: Code of Conduct'}, {'uid': 'A2TPQS65C609', 'name': '623: GASB 54 – Fund Balance'}, {'uid': 'AJ7AUF295E7E', 'name': '626: Federal Fiscal Compliance'}, {'uid': 'AJ7AUX295E87', 'name': '626.1: Travel Reimbursement - Federal Programs'}, {'uid': 'A2TPR365CF49', 'name': '705: Safety'}, {'uid': 'A2TPR765D529', 'name': '707: Use Of School Facilities'}, {'uid': 'A2TPRH65DF33', 'name': '716: Integrated Pest Management'}, {'uid': 'A2TPRK65E207', 'name': '718: Service Animals In Schools'}, {'uid': 'A2TPRU65EDB5', 'name': '801: Public Records'}, {'uid': 'A2TPS765FA18', 'name': '805: Emergency Preparedness'}, {'uid': 'A2TPS865FBC9', 'name': '806: Child/Student Abuse'}, {'uid': 'AJ7AUY295E88', 'name': '808: Food Services'}, {'uid': 'A2TPSJ66074B', 'name': '808.1: Free/Reduced-Price Meals And Free Milk'}, {'uid': 'A2TPT2661A21', 'name': '810.2: Transportation Video/Audio Monitoring'}, {'uid': 'A2TPT86620AB', 'name': '815: Technology Acceptable Use'}, {'uid': 'C7X36Y0569F6', 'name': '818: Contracted Services Personnel'}, {'uid': 'B75QDF618691', 'name': '819: Suicide Awareness, Prevention and Response'}, {'uid': 'B8FTJA69A669', 'name': '824: Maintaining Professional Adult/Student Boundaries'}, {'uid': 'A2TPTT66374F', 'name': '903: Public Participation In Board Meetings'}, {'uid': 'A2TPTX663BA6', 'name': '904: Public Attendance At School Events'}, {'uid': 'A2TPU46641A2', 'name': '907: School Visitors'}, {'uid': 'A2TPU7664536', 'name': '908: Relations With Parents/Guardians'}, {'uid': 'A2TPUG664F77', 'name': '913: Nonschool Organizations/Groups/Individuals'}, {'uid': 'BL5K555012AA', 'name': '913: Nonschool Organizations/Groups/Individuals'}, {'uid': 'AGWM8B59DF4D', 'name': '915: Booster/Support Groups'}, {'uid': 'A2TPUL6654E7', 'name': '917: Parental/Family Involvement'}]
#print(policy_menu_list)
for p in policy_menu_list:
    getDetail(mup, p['uid'])
