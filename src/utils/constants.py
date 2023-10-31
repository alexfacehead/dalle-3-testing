STATIC_CODE = """```py
def evaluate_image_improvement_v1(metrics):
    \"\"\"
    Evaluate the improvement of an image based on various metrics.
    
    Args:
    - metrics (dict): Dictionary containing values for various metrics.
    
    Returns:
    - score (float): A score indicating the degree of improvement. Higher values indicate more significant improvement.
    - summary (str): A textual summary of the evaluation.
    \"\"\"
    # Initialize the score
    score = 0
    
    # Handle MSE, Edge MSE, FFT MSE: Lower is better
    # Normalize by inverting the values and scaling down to a reasonable range
    score += 3 * (1 / (1 + metrics['mse'] / 20000))
    score += 3 * (1 / (1 + metrics['edge_mse'] / 20000))
    score += 3 * (1 / (1 + metrics['fft_mse'] / 1e9))
    
    # Handle SSIM: Higher is better
    score += 4 * metrics['ssim']
    
    # Handle PSNR: Higher is better
    # Normalize PSNR to a 0-1 scale (assuming max possible PSNR is 50)
    score += 3 * (metrics['psnr'] / 50)
    
    # Handle BRISQUE Difference: More negative is better for improvement
    # Normalize assuming BRISQUE difference ranges up to 100
    score += 4 * max(0, -metrics['brisque_diff'] / 100)
    
    # Handle Histogram Correlation: Closer to 1 is better
    # Normalize to 0-1 scale
    score += 2 * ((metrics['hist_corr'] + 1) / 2)
    
    # Handle Entropy: Higher is better
    score += metrics['entropy_diff'] / 10  # Normalize assuming entropy difference is up to 10
    
    # Handle MS-SSIM: Higher is better
    score += 4 * metrics['ms_ssim']
    
    # Handle GSIM: Higher is better
    score += 4 * metrics['gsim']
    
    # Handle VMAF: Higher is better
    score += 2.5 * (metrics['vmaf'] / 100)  # Assuming VMAF ranges from 0 to 100
    
    # Calculate average score
    total_weights = 3 + 3 + 3 + 4 + 3 + 4 + 2 + 2 + 4 + 4 + 5
    score /= total_weights  # Dividing by the sum of weights
    
    # Create a summary
    if score > 0.8:
        summary = "The improved image is significantly better than the base image."
    elif score > 0.5:
        summary = "The improved image shows notable enhancement compared to the base image."
    elif score > 0.2:
        summary = "The improved image has slight improvements over the base image."
    else:
        summary = "The improved image does not show clear improvements over the base image."
    
    return score, summary
    ```"""

SYSTEM_MESSAGE_MASTER = """In light of the context provided on artificial neural networks and their application in text-to-image generation, we have assembled a team of three experts with distinct skill sets to address your inquiries. They will collaborate in a 'tree-of-thought' manner, sharing their step-by-step insights with each other to provide you with the most comprehensive and accurate guidance. If any expert realizes their contribution is incorrect, they will promptly withdraw from the discussion.

Expert 1: I am an expert in artificial neural networks and their underlying architecture. I will focus on the foundational aspects of the machine learning algorithms and how they can be optimized for text-to-image generation.

Expert 2: I am an expert in prompt-based adjustments and context-specific optimization techniques. My contributions will revolve around refining the neural network's performance to align with desired outcomes through weight alterations and calculation fine-tuning.

Expert 3: I am an expert in evaluation metrics and image comparison methodologies. I will provide insights on assessing the generated results and guide the refinement process to improve the neural network's capabilities in producing accurate and relevant visual representations.

As you interact with our team of experts, feel free to ask questions or seek clarification on any aspect of artificial neural networks and their application in text-to-image generation. Our experts will collaborate and share their knowledge to ensure you receive the most accurate and coherent guidance possible."""

USER_MESSAGE_ONE = """Experts, please come to a consensus on the following question:

Can you design a team of experts capable of modifying evaluation metrics, which rely on pure statistics, without changing the underlying functionality? Instead, the goal is to tailor the code to align with a text prompt used for generating images, ensuring that the evaluation metric code is better suited for that specific context. This is intended for an advanced text-to-image artificial neural network, where the objective is to adjust the code based on a given prompt so that the resulting image can be more accurately compared to another version of the prompt. Some prompts may require fine-tuned metrics, so the system should be designed in a way that only alters weights and potentially some calculations, without fundamentally changing the code."""

ASSISTANT_MESSAGE_ONE = """Expert 1: As an expert in artificial neural networks, I understand the importance of having a well-suited evaluation metric for the task at hand. In this case, the task is text-to-image generation, and the goal is to adjust the evaluation metric code based on a given prompt to improve the comparison between generated images.

Expert 2: As an expert in prompt-based adjustments, I can suggest that one approach to achieve this goal is to create a meta-learning system that can learn to adjust the evaluation metric based on the prompt. This system would take the prompt and the current evaluation metric as inputs and output a modified evaluation metric that is better suited for the specific context. The modifications can include altering weights and fine-tuning calculations, as long as the underlying functionality remains unchanged.

Expert 3: As an expert in evaluation metrics, I can confirm that this approach seems feasible. By designing a meta-learning system that can adapt the evaluation metric based on the prompt, we can ensure that the metric is more sensitive to the specific context and can provide a more accurate comparison between generated images. This will ultimately help improve the performance of the text-to-image artificial neural network.

In summary, our consensus is that it is possible to design a team of experts capable of modifying evaluation metrics without changing the underlying functionality. The key is to develop a meta-learning system that can adapt the evaluation metric based on the given prompt, allowing for more accurate comparisons between generated images. This system should focus on altering weights and fine-tuning calculations while preserving the core functionality of the evaluation metric code."""

USER_MESSAGE_TWO = """Great. Given the following:

Given a textual prompt, such as "Can you create an image of a pendulum board with crystal pendulum swinging over with a witch with long blonde hair using it," analyze the provided Python code for evaluating the improvement of an image based on various metrics. The code takes a dictionary of metrics as input and calculates a weighted score to determine the degree of improvement. Consider the following aspects while analyzing the code:

1. Are the chosen metrics - without removing any metrics or adding any paremeters - appropriate for evaluating image improvement, considering the varying nature of the textual prompts?
2. Are the weights assigned to each metric reasonable in the context of different prompts?
3. Can the normalization techniques used for each metric be improved to better handle varying prompts?
4. Can the code be refactored or optimized for better readability or performance, given the varying nature of the prompts?

Additionally, provide suggestions for modifying the code, such as altering the weights, normalization techniques, or incorporating new metrics, to improve the evaluation of image improvement in the context of varying prompts. Keep in mind the following feedback when providing suggestions:

1. Try your best not to omit metrics, and *do not* add new parameters. Retain the integrity of the original structure.
2. For the MSE, Edge MSE, and FFT MSE, you may want to experiment with different scaling factors to better balance their contributions to the overall score.
3. The PSNR normalization assumes a maximum value of 50. You may want to make this value adjustable or use a more adaptive normalization technique.
4. The BRISQUE difference normalization assumes a range up to 100. You may want to verify if this range is appropriate for your dataset or adjust it accordingly.
5. The entropy difference normalization assumes a range up to 10. You may want to verify if this range is appropriate for your dataset or adjust it accordingly.
6. Consider adding comments to explain the choice of weights and normalization techniques for each metric.

Ensure that your suggestions can be easily integrated with the existing code without requiring a complete overhaul of the code structure and can adapt to the varying nature of textual prompts.

This includes avoiding adding contrived or unnecessary functions or parameters. Focus on altering the metrics as they are in relation to the original text prompt provided to you below, using your semantic analysis skills.

Here is the code in question, with the prompt `{}`:

And here is the code to be updated using your skills, the provided context, etc:\n\n"""

USER_MESSAGE_TWO = USER_MESSAGE_TWO + STATIC_CODE + "\n\n" + "Without introducing new parameters, can you update this code, especially when taking into consideration the basal prompt provided earlier?"

DEFAULT_PLACEHOLDER_PROMPT = "Make an image."
AI_FILE_IMPORTS = """"""

SYSTEM_MESSAGE_GPT_3_5 = """You follow your user's directions precisely, returning only what they request."""

USER_FEEDBACK_SMALL = """Return only the code, without backticks, that is in the below text. I will surround the text with triple quotes, but don't include those.\n\n"""