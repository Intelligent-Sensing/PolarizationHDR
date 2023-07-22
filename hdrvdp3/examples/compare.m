function [] = compare(ref_file, comp_file, save_path)


% This example demonstrates how HDR-VDP can be used to detect impairments
% in HDR images. The results are shown separately for side-by-side and
% flicker detection tasks.
%
% Note that the predicted visibility of introduced distortions may not much 
% the visibility of those seen on the screen. The HDR images are scaled in
% absolute photometric units and parts of the image are much darker than
% shown in tone-mapped images, making distortions less visible.

if ~exist( 'hdrvdp3', 'file' )
    addpath( fullfile( pwd, '..') );
end

% Display parameters
Y_peak = 200;     % Peak luminance in cd/m^2 (the same as nit)
contrast = 1000;  % Display contrast 1000:1
gamma = 2.2;      % Standard gamma-encoding
E_ambient = 100;  % Ambient light = 100 lux


% I_ref = hdrread(ref_file);
I_ref= double(imread(ref_file))/255;

% Make the image smaller so that we can fit more on the screen
% I_ref = max( imresize( I_ref, 0.5, 'lanczos2' ), 0.0001 );

% Find the angular resolution in pixels per visual degree:
% 30" 4K monitor seen from 0.5 meters
ppd = hdrvdp_pix_per_deg( 30, [3840 2160], 0.5 );

% Noise

% Create test image with added noise
% I_test = hdrread(comp_file);
I_test= double(imread(comp_file))/255;
% noise = randn(size(I_ref,1),size(I_ref,2)) .* get_luminance( I_ref ) * 0.2;
% I_test_noise = max( I_ref + repmat( noise, [1 1 3] ), 0.0001 );
L_ref = hdrvdp_gog_display_model( I_ref, Y_peak, contrast, gamma, E_ambient );
L_test= hdrvdp_gog_display_model( I_test, Y_peak, contrast, gamma, E_ambient );

res_sbs = hdrvdp3( 'side-by-side', L_test, L_ref, 'rgb-native', ppd );
display(res_sbs.P_det)
display(res_sbs.Q)
% res_noise_flicker = hdrvdp3( 'flicker', I_test_noise, I_ref, 'rgb-native', ppd );

% context image to show in the visualization
I_context = get_luminance( I_ref );

% Visualize images assuming 200 cd/m^2 display
% This size is not going to be correct because we are using subplot
gamma = 2.2;
L_peak = 200; 

clf
% subplot( 2, 3, 1 );
% imshow( (I_test_noise/L_peak).^(1/gamma) );
% title( 'Noisy image' );

% subplot( 2, 3, 2 );
% imshow( hdrvdp_visualize( res_noise_sbs.P_map, I_context ) );
% title( 'Noise, task: side-by-side' );

out_img = hdrvdp_visualize( res_sbs.P_map, I_context );
imwrite(out_img, strrep(save_path, '.png', strcat('_', string(res_sbs.P_det), '_', string(res_sbs.Q), '.png')));
% subplot( 2, 3, 3 );
% imshow( hdrvdp_visualize( res_noise_flicker.P_map, I_context ) );
% title( 'Noise, task: flicker' );

% subplot( 2, 3, 4 );
% imshow( (I_test_blur/L_peak).^(1/gamma) );
% title( 'Blurry image' );

% subplot( 2, 3, 5 );
% imshow( hdrvdp_visualize( res_blur_sbs.P_map, I_context ) );
% title( 'Blur, task: side-by-side' );

% subplot( 2, 3, 6 );
% imshow( hdrvdp_visualize( res_blur_flicker.P_map, I_context ) );
% title( 'Blur, task: flicker' );







% % Detect contrast loss, amplification and reversal for a pair of HDR and
% % tone-mapped images. 
% %
% % This example demonstrates 'civdm' mode - Contrast Invariant Visibility
% % Difference Metric, which is a variation of the Dynamic Range Independent
% % Metric from the paper:
% %
% % T. O. Aydin, R. Mantiuk, K. Myszkowski, and H.-P. Seidel, 
% % "Dynamic range independent image quality assessment", 
% % ACM Trans. Graph. (Proc. SIGGRAPH), vol. 27, no. 3, p. 69, 2008.

% if ~exist( 'hdrvdp3', 'file' )
%     addpath( fullfile( pwd, '..') );
% end

% %I_hdr = hdrread( 'nancy_church.hdr' );
% I_hdr = hdrread(ref_file);

% I_tmo = cell(1,1);
% I_tmo{1} = double(imread(comp_file))/255;
% %I_tmo{1} = double(imread( 'nancy_church_mai11.png' ))/255;
% %I_tmo{2} = double(imread( 'nancy_church_saturated.png' ))/255;
% %I_tmo{3} = double(imread( 'nancy_church_mantiuk06.png' ))/255;


% % Run the Contrast Invariant Visibility Difference Metric on each
% % tone-mapped image
% res = cell(length(I_tmo),1);
% vis = cell(length(I_tmo),1);
% for kk=1:length(I_tmo)
%     fprintf( 1, '.' );
    
%     % Find the angular resolution in pixels per visual degree:
%     % 30" 4K monitor seen from 0.5 meters
%     ppd = hdrvdp_pix_per_deg( 30, [3840 2160], 0.5 ); 
    
%     % Convert from gamma corrected pixel values stored in SDR images 
%     % to linear colorimetric values shown on a display with the peak
%     % luminance of 200 cd/m^2
%     Y_tone_mapped = hdrvdp_gog_display_model( I_tmo{kk}, 200 );
    
%     tic;
%     res{kk} = hdrvdp3( 'civdm', Y_tone_mapped, I_hdr, 'rgb-native', ppd );
%     toc
   
%     vis{kk} = hdrvdp_visualize( 'pmap', res{kk}.pmap, I_hdr );
% end
% fprintf( 1, '\n' );

% clf
% %imshow( cat( 1, cat( 2, I_tmo{1}, I_tmo{2}, I_tmo{3} ) , cat( 2, vis{1}, vis{2}, vis{3} ) ) )
% %title( 'Predictions for an image tone-mapped with three different operators' );
% imwrite(vis{1}, '../out/tmo1.png');
% % imwrite(vis{2}, '../out/tmo2.png');
% % imwrite(vis{3}, '../out/tmo3.png');