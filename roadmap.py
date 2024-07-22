client_name="Fuad "
prompt="""You are a visa expert whose role is to explain to client their visa roadmap which was drafted by a 
solution architect(the person who makes visa roadmaps based on client information), go through the roadmap and  explain
the points and the insights, explain to the client what various technical terms on the roadmap mean and imply,
what are their weaknesses and strengths and what steps can they take to improve. 
This is how the conversation will go - 
You will greet the user ask shall we move to their roadmap (Don't start the roadmap until you get their confirmation).
Then you will explain one section at a time, Also every now and then, pause for the user to understand the
information and ask them if they are following along or if they have any questions. Answer any cross question that the client has,
and if they don't have a follow up question, continue explaining the roadmap. 
Keep your explanations short and to the point and leave room for more elaboration only when user asks.
Following is the visa roadmap:
"""
roadmap=""""
Visa Roadmap for Fuad
 1. Client Information
 •  Name: Jali-Ligali Nafisat Temitope
 •  Age: 33 (as of September 18, 2022)
 •  Marital Status: Married
 •  Product Type: Express Entry (EE)/ Provincial Nominee Program (PNP)
 •  Projected CRS Score: To be determined based on IELTS scores and work experience
 assessment.
 •  Current PA IELTS Scores: Listening - 8.5, Reading - 8.0, Speaking - 7.5, Writing - 7.5
 •  Current Spouse IELTS Scores: Listening - 8.0, Reading - 7.0, Speaking - 7.0, Writing 
7.0
 •  Available Education: Master's degree (Principal Applicant), Bachelor's degree (Spouse)
 •  Years of Work Experience: More than 3 years (Principal Applicant)
 •  Previous Canada application: None
 •  Additional Information: Residing in Nigeria.
 2. Projected IELTS Scores
 •  Listening: 8.5 (PA), 8.0 (Spouse)
 •  Reading: 8.0 (PA), 7.0 (Spouse)
 •  Writing: 7.5 (PA), 7.0 (Spouse)
 •  Speaking: 7.5 (PA), 7.0 (Spouse)
 3. Required Minimum IELTS Scores
 •  Listening: 7.0 (PA & Spouse)
 •  Speaking: 7.0 (PA & Spouse)
 •  Reading: 7.0 (PA & Spouse)
 •  Writing: 7.0 (PA & Spouse)
 4. Recommended Pathways
 •  Option A: Express Entry (EE) - Federal Skilled Worker Program (FSWP)
 Justification: Your strong IELTS scores and Master's degree will likely grant you
 a high CRS score, making you eligible for an ITA (Invitation to Apply) under EE.
 •  Option B: Provincial Nominee Program (PNP)
 Justification: Consider exploring PNP streams in provinces like Ontario, Alberta,
 or British Columbia, which often have specific occupations in demand. This could
 offer a faster pathway to PR.
 •  Option C: EE + PNP Combination
 Justification: Create an EE profile and simultaneously apply for a PNP
 nomination. If you receive a PNP nomination, it will significantly boost your CRS
 score, increasing your chances of receiving an ITA.
 5. Recommended NOC
 •  Option A: FSWP (EE)
NOC 2141 - University Professors and Teachers: If your work experience aligns
 with teaching or research in a university setting, this NOC could be a strong fit.
 NOC 2142 - Post-Secondary Education Teachers: Consider this NOC if your
 work experience is in teaching at a college or technical institute.
 •  Option B: PNP (Ontario)
 NOC 2141 - University Professors and Teachers: Ontario has a specific PNP
 stream for skilled professionals in this field.
 NOC 2142 - Post-Secondary Education Teachers: This NOC is also in demand
 in Ontario.
 •  Option C: PNP (Alberta)
 NOC 2141 - University Professors and Teachers: Alberta's PNP stream for
 skilled workers often includes this NOC.
 NOC 2142 - Post-Secondary Education Teachers: Alberta also has a need for
 post-secondary education teachers.
 6. Additional Information
 •  Credential Evaluation: Get your educational credentials evaluated by a designated
 organization like WES or ICAS to ensure they meet Canadian standards.
 •  Work Experience Assessment: If your work experience is not directly related to your
 educational qualifications, consider getting it assessed by a designated organization like
 ECA.
 •  Proof of Funds: You will need to demonstrate sufficient funds to support yourself and
 your family in Canada.
 •  Medical Examination: You will need to undergo a medical examination from a
 designated doctor.
 •  Police Clearance Certificate: Obtain a police clearance certificate from your country
 of origin.
 7. Timelines
 •  Eligibility Requirements Completion (Month 1-3):
 Credential evaluation
 Language test completion
 NOC selection
 Work experience assessment (if needed)
 •  Pre-ITA Stage (Month 3-6):
 Profile creation on the EE portal
 Profile review and submission
 Application for PNP nomination (if applicable)
 •  ITA and Documentation (Month 6-9):
 Document review and preparation
 Post-ITA profile completion and submission
 •  Biometrics Request (Month 9-12):
Biometrics completion
 •  Passport Request (PPR) (Month 12-18):
 Document submission and processing
 •  Confirmation of Permanent Residency (COPR) (Month 18-24):
 Visa approval and passport return
 Note: Processing times can vary significantly depending on the program and individual
 circumstances. Delays can occur due to third-party processing times, such as credential
 evaluation or provincial processing.
 Client-Specific Notes:
 •  Your strong IELTS scores and Master's degree are significant strengths for both EE and
 PNP programs.
 •  Consider exploring PNP streams in provinces where your occupation is in demand.
 •  Be prepared
"""

full_prompt=prompt+roadmap