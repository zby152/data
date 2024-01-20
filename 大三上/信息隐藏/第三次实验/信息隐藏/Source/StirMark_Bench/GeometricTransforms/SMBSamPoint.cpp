//////////////////////////////////////////////////////////////////////
// StirMark Benchmark - SMBSamPoint.cpp
//
// Contents: Implementation of the CSMBSamPoint class
//
// Purpose:  See SMBSamPoint.h
//
// Created:  Fabien A. P. Petitcolas, Microsoft Research, March 2000
//
// Modified: Nazim Fat�s, Microsoft Research
//
// History: 
//
// Copyright (c) 2000-2002, Microsoft Research Ltd , Institut National
// de Recherche en Informatique et Automatique (INRIA), Institut Eur�com
// and the Integrated Publication and Information Systems Institute at
// GMD - Forschungszentrum Informationstechnik GmbH (GMD-IPSI).
// 
// Redistribution and use in source and binary forms, with or without
// modification, are permitted for non-commercial research and academic
// use only, provided that the following conditions are met:
// 
// - Redistributions of source code must retain the above copyright
//   notice, this list of conditions and the following disclaimer. Each
//   individual file must retain its own copyright notice.
// 
// - Redistributions in binary form must reproduce the above copyright
//   notice, this list of conditions, the following disclaimer and the
//   list of contributors in the documentation and/or other materials
//   provided with the distribution.
// 
// - Modification of the program or portion of it is allowed provided
//   that the modified files carry prominent notices stating where and
//   when they have been changed. If you do modify this program you
//   should send to the contributors a general description of the changes
//   and send them a copy of your changes at their request. By sending
//   any changes to this program to the contributors, you are granting a
//   license on such changes under the same terms and conditions as
//   provided in this license agreement. However, the contributors are
//   under no obligation to accept your changes.
// 
// - All non-commercial advertising materials mentioning features or use
//   of this software must display the following acknowledgement:
// 
//     This product includes software developed by Microsoft Research
//     Ltd, Institut National de Recherche en Informatique et Automatique
//     (INRIA), Institut Eur�com and the Integrated Publication and
//     Information Systems Institute at GMD - Forschungszentrum
//     Informationstechnik GmbH (GMD-IPSI).
// 
// - Neither name of Microsoft Research Ltd, INRIA, Eur�com and GMD-IPSI
//   nor the names of their contributors may be used to endorse or
//   promote products derived from this software without specific prior
//   written permission.
// 
// - If you use StirMark Benchmark for your research, please cite:
// 
//     Fabien A. P. Petitcolas, Martin Steinebach, Fr�d�ric Raynal, Jana
//     Dittmann, Caroline Fontaine, Nazim Fat�s. A public automated
//     web-based evaluation service for watermarking schemes: StirMark
//     Benchmark. In Ping Wah Wong and Edward J. Delp, editors,
//     proceedings of electronic imaging, security and watermarking of
//     multimedia contents III, vol. 4314, San Jose, California, U.S.A.,
//     20-26 January 2001. The Society for imaging science and
//     technology (I.S.&T.) and the international Society for optical
//     engineering (SPIE). ISSN 0277-786X.
// 
// and
// 
//     Fabien A. P. Petitcolas. Watermarking schemes
//     evaluation. I.E.E.E. Signal Processing, vol. 17, no. 5,
//     pp. 58-64, September 2000.
// 
// THIS SOFTWARE IS NOT INTENDED FOR ANY COMMERCIAL APPLICATION AND IS
// PROVIDED BY MICROSOFT RESEARCH LTD, INRIA, EUR�COM, GMD-IPSI AND
// CONTRIBUTORS 'AS IS', WITH ALL FAULTS AND ANY EXPRESS OR IMPLIED
// REPRESENTATIONS OR WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED REPRESENTATIONS OR WARRANTIES OF MERCHANTABILITY AND FITNESS
// FOR A PARTICULAR PURPOSE, TITLE OR NONINFRINGEMENT OF INTELLECTUAL
// PROPERTY ARE DISCLAIMED. IN NO EVENT SHALL MICROSOFT RESEARCH LTD,
// INRIA, EUR�COM, GMD-IPSI OR THEIR CONTRIBUTORS BE LIABLE FOR ANY
// DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
// GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
// IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
// OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
// ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// 
// THE USE OF THIS SOFTWARE FOR CIRCUMVENTING WITHOUT AUTHORITY ANY
// EFFECTIVE TECHNOLOGICAL MEASURES DESIGNED TO PROTECT ANY COPYRIGHTS OR
// ANY RIGHTS RELATED TO COPYRIGHT AS PROVIDED BY LAW OR THE SUI GENERIS
// RIGHT PROVIDED BY SOME COUNTRIES IS STRICTLY PROHIBITED.
//
// $Header: /home/cvs/StirmarkBench/StirMark_Bench/GeometricTransforms/SMBSamPoint.cpp,v 1.12 2002/04/19 10:23:57 petitcolas Exp $
//////////////////////////////////////////////////////////////////////



// STL headers

// Other standard headers

// STL headers
#include "SMBSamPoint.h"
#include "SMBTransformer.h"
#include "SMBReconstructor.h"
#include "../Base/SMBImage.h"
#include "../Base/SMBTools.h"
#include "../Base/SMBTypes.h"



//////////////////////////////////////////////////////////////////////
// Constructor / destructor
//////////////////////////////////////////////////////////////////////
CSMBSamPoint::CSMBSamPoint()
  : CSMBResampler()
{

}


CSMBSamPoint::~CSMBSamPoint()
{

}

//////////////////////////////////////////////////////////////////////
// Main function: compute the coordinates of the pixels of the
// output inmage in the old image
//////////////////////////////////////////////////////////////////////
int CSMBSamPoint::Resample(const CSMBImage&          in_imgOriginal,
                                 CSMBImage&         out_imgTransformed,
                           const CSMBReconstructor&  in_rec,
                           const CSMBTransformer&    in_tra            ) const
{
  long Y = out_imgTransformed.NumberOfRows();
  long X = out_imgTransformed.NumberOfColumns();
  long C = out_imgTransformed.NumberOfChannels();

  // For all pixels in output image
  for (long y = 0; y < Y; y++)
  {
    for (long x = 0; x < X; x++)
    {
      for (long ch = 0; ch < C; ch++)
      {
        // Compute the coordinates of the pixel in the original image
        dVector newXY = in_tra.XYTransfo1((double)x + 0.5 + m_xOffset, 
                                          (double)y + 0.5 + m_yOffset);
        
        // Compute the value of the original picture at this place
        double dNewVal = in_rec.Reconstruct(newXY.x, newXY.y, ch, in_imgOriginal);

        // Thresholding
        Gray iNewVal = RoundClip(dNewVal);

        // Setting the color in the target image
        out_imgTransformed.SetPixel(x, y, ch, iNewVal);
      } // for ch
    } // for x
  } // for y
  return (SMBSUCCESS);
}
