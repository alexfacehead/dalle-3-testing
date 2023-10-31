# Essentials for computation
import os
# Essentials for running VMAF models the ground-up way
from src.metrics import metric_calculations
# Formatting output
from termcolor import colored
# Helpers and AI-adaptive code
from src.evaluation_metrics import evaluate_image_improvement, compare_images

# Necessary constants
from src.utils.constants import DEFAULT_PLACEHOLDER_PROMPT

# Import and initialize env variables
from dotenv import load_dotenv

env_found = load_dotenv()
AI_ASSISTED = os.getenv('AI_ENHANCED_EVALUATION')

def compare_all_images(reference_directory, generated_directory):
    print("Entered compare all_images ...")
    if not os.path.exists(reference_directory) or not os.path.exists(generated_directory):
        print(f"Error: One or both of the directories {reference_directory} and {generated_directory} do not exist.")
        return
    print("Passed OS directory check for compare_all_images ...")
    reference_images = sorted(os.listdir(reference_directory))
    generated_images = sorted(os.listdir(generated_directory))

    reference_dict = {img.split('_base')[0]: img for img in reference_images}
    generated_dict = {img.split('_improved')[0]: img for img in generated_images}
    print("Reference Dict Keys:", reference_dict.keys())
    print("Generated Dict Keys:", generated_dict.keys())
    print("Common Keys:", reference_dict.keys() & generated_dict.keys())
    print("Generated dictionary properly ...")
    # Initialize the dictionary to hold the sum of each metric
    metric_sums = {
        'mse': 0,
        'ssim': 0,
        'psnr': 0,
        'brisque_diff': 0,
        'hist_corr': 0,
        'edge_mse': 0,
        'entropy_diff': 0,
        'fft_mse': 0,
        'ms_ssim': 0,
        'gsim': 0,
        'vmaf': 0
    }

    num_comparisons = 0
    print("Pre-entering key block ...")
    for key in reference_dict.keys() & generated_dict.keys():
        print("Entered key block of compare_all_images ...")
        ref_img_path = os.path.join(reference_directory, reference_dict[key])
        gen_img_path = os.path.join(generated_directory, generated_dict[key])

        results = compare_images(ref_img_path, gen_img_path)
        if results:
            num_comparisons += 1
            mse_value, ssim_value, psnr_value, brisque_value_image1, brisque_value_image2, hist_corr_value, colorfulness_image1, colorfulness_image2, edge_mse_value, entropy_image1, entropy_image2, fft_mse_value, brisque_diff, ms_ssim_value, gsim_value, vmaf_value = results
            
            # Print comparison details
            print(f"Comparing {reference_dict[key]} and {generated_dict[key]}:")
            print(f"  MSE: {mse_value}")
            print(f"  SSIM: {ssim_value}")
            print(f"  PSNR: {psnr_value}")
            print(f"  BRISQUE Difference (Improved - Base): {brisque_diff}")
            print(f"  Histogram Correlation: {hist_corr_value}")
            print(f"  Colorfulness for {reference_dict[key]}: {colorfulness_image1}")
            print(f"  Colorfulness for {generated_dict[key]}: {colorfulness_image2}")
            print(f"  Edge MSE: {edge_mse_value}")
            print(f"  Entropy for {reference_dict[key]}: {entropy_image1}")
            print(f"  Entropy for {generated_dict[key]}: {entropy_image2}")
            print(f"  FFT MSE: {fft_mse_value}")
            print(f"  MS-SSIM: {ms_ssim_value}")
            print(f"  GSIM: {gsim_value}")
            print(f"  VMAF: {vmaf_value}")
            
            # Extract metrics and evaluate improvement
            metrics = {
                'mse': mse_value,
                'ssim': ssim_value,
                'psnr': psnr_value,
                'brisque_diff': brisque_diff,
                'hist_corr': hist_corr_value,
                'edge_mse': edge_mse_value,
                'entropy_diff': entropy_image2[0] - entropy_image1[0],  # Difference in entropy
                'fft_mse': fft_mse_value,
                'ms_ssim': ms_ssim_value,
                'gsim': gsim_value,
                'vmaf': vmaf_value
            }

            # Update metric_sums
            for metric, value in metrics.items():
                metric_sums[metric] += value
            
            score, summary = evaluate_image_improvement(metrics, prompt="Make a hyper realistic  beautiful spotted bengal cat with green eyes ")
            # Initialize secondary, AI-altered computation score and summaries to None
            score_v2 = None
            summary_v2 = None
            if AI_ASSISTED:
                from ai_adjusted_eval_metric import evaluate_image_improvement_v2
                score_v2, summary_v2 = evaluate_image_improvement_v2(metrics)
                print("Updated evaluation metric used.")
            # Print the summary in red
            res_string_printed = f"{summary} (Score: {score:.16f})"
            res_string_printed_v2 = f"AI-altered metric summary:\n\n {summary_v2} (Score: {score_v2:.16f})"
            print(colored(res_string_printed, 'red'))
            print(colored(res_string_printed_v2, 'green'))
            print()
            if num_comparisons > 0: # Alter to return running total averages only near the end
                metric_averages = {metric: value / num_comparisons for metric, value in metric_sums.items()}
                print(colored("RUNNING TOTAL AVERAGE ACROSS IMAGE DATASET", 'magenta'))
                for metric, average in metric_averages.items():
                    print(f"{metric.upper()}: {average:.16f}")

                # Get the score and summary
                score, summary = evaluate_image_improvement(metric_averages, prompt=DEFAULT_PLACEHOLDER_PROMPT)

                # Format the score to four decimal places when printing
                conclusion_str = f"Conclusion on running total average for images: {summary} (Score: {score:.16f})"
                print(colored(conclusion_str, 'green'))

    print("Completed compare_all_images ...")


def main():
    default_reference_directory = os.path.join(os.getcwd(), "src/resources/base")
    default_generated_directory = os.path.join(os.getcwd(), "src/resources/improved")
    default_generated_text_prompts = os.path.join(os.getcwd(), "src/resources/prompt_keys")

    reference_directory = input(f"Enter the path to your reference images directory (default: {default_reference_directory}): ") or default_reference_directory
    generated_directory = input(f"Enter the path to your generated images directory (default: {default_generated_directory}): ") or default_generated_directory
    default_generated_text_prompts = input(f"Enter the path to your prompts directory (default: {default_generated_text_prompts}): ") or default_generated_text_prompts

    compare_all_images(reference_directory, generated_directory)

if __name__ == "__main__":
    main()