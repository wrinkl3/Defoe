/*
 * This file is part of the LIRE project: http://lire-project.net
 * LIRE is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * LIRE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with LIRE; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * We kindly ask you to refer the any or one of the following publications in
 * any publication mentioning or employing Lire:
 *
 * Lux Mathias, Savvas A. Chatzichristofis. Lire: Lucene Image Retrieval –
 * An Extensible Java CBIR Library. In proceedings of the 16th ACM International
 * Conference on Multimedia, pp. 1085-1088, Vancouver, Canada, 2008
 * URL: http://doi.acm.org/10.1145/1459359.1459577
 *
 * Lux Mathias. Content Based Image Retrieval with LIRE. In proceedings of the
 * 19th ACM International Conference on Multimedia, pp. 735-738, Scottsdale,
 * Arizona, USA, 2011
 * URL: http://dl.acm.org/citation.cfm?id=2072432
 *
 * Mathias Lux, Oge Marques. Visual Information Retrieval using Java and LIRE
 * Morgan & Claypool, 2013
 * URL: http://www.morganclaypool.com/doi/abs/10.2200/S00468ED1V01Y201301ICR025
 *
 * Copyright statement:
 * ====================
 * (c) 2002-2013 by Mathias Lux (mathias@juggle.at)
 *  http://www.semanticmetadata.net/lire, http://www.lire-project.net
 *
 * Updated: 07.11.14 14:43
 */

package net.semanticmetadata.lire.sampleapp;

import net.semanticmetadata.lire.imageanalysis.features.GlobalFeature;
import net.semanticmetadata.lire.utils.FileUtils;
import org.apache.commons.lang3.ArrayUtils;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.concurrent.ExecutionException;

/**
 * This file is part of LIRE, a Java library for content based image retrieval.
 *
 * @author Mathias Lux, mathias@juggle.at, 07.11.2014
 */
public class ExtractDefacementFeatures {

    public static String[] featureNames = {"global.SimpleColorHistogram", "global.EdgeHistogram", "global.Tamura", "global.Gabor"};


    private static void extractBulk(String directoryPath) throws IOException{
        ArrayList<String> images = FileUtils.getAllImages(new File(directoryPath), true);
        GlobalFeature[] features = getFeatureClasses();
        for (Iterator<String> it = images.iterator(); it.hasNext(); ) {
            double[] arr = new double[0];
            String imageFilePath = it.next();
            //System.out.println("Indexing " + imageFilePath);
            for (GlobalFeature f : features) {
                BufferedImage img = ImageIO.read(new FileInputStream(imageFilePath));
                //System.out.println("Extracting " + f.getClass().getName() + ".");
                f.extract(img);
                arr = ArrayUtils.addAll(arr, f.getFeatureVector());
                //System.out.println(f.getFeatureVector().length);
            }
            //System.out.println(arr.length);
            String res = Arrays.toString(arr).replace(",","").replace("[","").replace("]", "");
            //String res = Arr2String(arr);
            System.out.println(res);
        }
    }

    private static void extractSingle(String imagePath) throws IOException{
        BufferedImage img = ImageIO.read(new FileInputStream(imagePath));
        GlobalFeature[] features = getFeatureClasses();
        double[] arr = new double[0];
        for (GlobalFeature f : features) {
            //System.out.println("Extracting " + f.getClass().getName() + ".");
            f.extract(img);
            System.out.println(f.getFeatureVector().length);
            arr = ArrayUtils.addAll(arr, f.getFeatureVector());
            //System.out.println(f.getFeatureVector().length);
        }
        String res = Arrays.toString(arr).replace(",","").replace("[","").replace("]", "");
        //String res = Arr2String(arr);
        System.out.println(res);
    }



    public static void main(String[] args) throws IOException {
        boolean bulk = false;
        String path = null;
        String[] features = new String[0];
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if (arg.startsWith("-p")) {
                try {
                    path = args[i+1];
                } catch (Exception e) {
                    e.printStackTrace();
                    printHelp();
                }
            }
            else if (arg.startsWith("--b")){
                bulk = true;
            }
        }
        if(bulk){
            extractBulk(path);
        }
        else{
            extractSingle(path);
        }

    }

    private static GlobalFeature[] getFeatureClasses(){
        GlobalFeature[] features = new GlobalFeature[featureNames.length];
        for (int i = 0; i < featureNames.length; i++) {
            try {
                features[i] = (GlobalFeature) Class.forName("net.semanticmetadata.lire.imageanalysis.features." + featureNames[i]).newInstance();
            } catch (Exception e) {
                e.printStackTrace();
                printHelp();
            }
        }
        return features;
    }

    private static String Arr2String(double[] arr){
        String res = "";
        for(double d : arr){
            res+=Double.toString(d)+" ";
        }
        res = res.trim();
        return res;
    }

    private static void printHelp() {
        System.exit(1);
    }
}

