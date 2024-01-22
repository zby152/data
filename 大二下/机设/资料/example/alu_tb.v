`timescale 1ns/1ns

// testbench for simulation
module alu_tb();
    
   reg  signed [31:0] A, B;
   reg  [2:0]  ALUOp;
   wire [31:0] C;
   wire Zero;
    
// instantiation of alu    
   alu U_ALU(
             .A(A), .B(B), .ALUOp(ALUOp), .C(C), .Zero(Zero)      
   );
   
   initial begin
   A=32'd2;
   B=32'd13;
   ALUOp=3'b000;
   
   end
   

   always begin
    #(50) ALUOp = ALUOp+1;
   end //end always
   
endmodule
