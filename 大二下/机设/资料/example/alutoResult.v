
module alutoResult( A, B, ALUOp, clk, rst, Zero, Result);
   input signed [31:0] A, B;
   input [2:0]  ALUOp;
   input clk, rst;
   output Zero;
   output [31:0] Result;

   wire [31:0] aluoutC;

    
// instantiation    
   alu U_ALU(
       .A(A), .B(B), .ALUOp(ALUOp), .C(aluoutC), .Zero(Zero)      
   );
   
   result U_RESULT(

      .clk(clk), .rst(rst), .aluoutC(aluoutC), .Result(Result)
     );

      
endmodule
