
def evaluate_image_improvement_v2(metrics):
    score = 0
    mse_weight = 3
    edge_mse_weight = 3
    fft_mse_weight = 3
    score += mse_weight * (1 / (1 + metrics['mse'] / 20000))
    score += edge_mse_weight * (1 / (1 + metrics['edge_mse'] / 20000))
    score += fft_mse_weight * (1 / (1 + metrics['fft_mse'] / 1e9))
    ssim_weight = 4
    score += ssim_weight * metrics['ssim']
    psnr_weight = 3
    max_psnr = 50
    score += psnr_weight * (metrics['psnr'] / max_psnr)
    brisque_diff_weight = 4
    max_brisque_diff = 100
    score += brisque_diff_weight * max(0, -metrics['brisque_diff'] / max_brisque_diff)
    hist_corr_weight = 2
    score += hist_corr_weight * ((metrics['hist_corr'] + 1) / 2)
    entropy_diff_weight = 1
    max_entropy_diff = 10
    score += entropy_diff_weight * (metrics['entropy_diff'] / max_entropy_diff)
    ms_ssim_weight = 4
    score += ms_ssim_weight * metrics['ms_ssim']
    gsim_weight = 4
    score += gsim_weight * metrics['gsim']
    vmaf_weight = 2.5
    max_vmaf = 100
    score += vmaf_weight * (metrics['vmaf'] / max_vmaf)
    total_weights = mse_weight + edge_mse_weight + fft_mse_weight + ssim_weight + psnr_weight + brisque_diff_weight + hist_corr_weight + entropy_diff_weight + ms_ssim_weight + gsim_weight + vmaf_weight
    score /= total_weights
    if score > 0.8:
        summary = "The improved image is significantly better than the base image."
    elif score > 0.5:
        summary = "The improved image shows notable enhancement compared to the base image."
    elif score > 0.2:
        summary = "The improved image has slight improvements over the base image."
    else:
        summary = "The improved image does not show clear improvements over the base image."
    return score, summary