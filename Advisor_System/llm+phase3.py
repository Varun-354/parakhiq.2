from phase_3 import full_resume_analysis
# from phase_5 import ask_llm,get_analysis_prompt

# Step 1: Run Phase 3
result = full_resume_analysis("sample_resume.txt")

predicted_role = result["predicted_role"]
skills = result["skills"]

# Step 2: Read Resume Text
resume_text = open("sample_resume.txt").read()

# # Step 3: Generate Prompt
# prompt = get_analysis_prompt(resume_text, predicted_role)

# # Step 4: Call LLM
# llm_feedback = ask_llm(prompt)

# Step 5: Final Output
final_result = {
    **result,
    "llm_feedback": llm_feedback
}

print(final_result)




