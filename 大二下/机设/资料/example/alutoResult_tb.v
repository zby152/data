`timescale 1ns/1ns

// testbench for simulation
module alutoResult_tb();
    
   reg  signed [31:0] A, B;
   reg  [2:0]  ALUOp;
   reg clk;
   reg rst;
   wire Zero;
   wire [31:0] Result;
    
// instantiation of alutoResult    
   alutoResult U_ALUTORESULT(
      .A(A), .B(B), .ALUOp(ALUOp), .clk(clk), .rst(rst), .Zero(Zero), .Result(Result)
       );
   
   initial begin
     A=32'd2;
     B=32'd13;
     ALUOp=3'b000;
     clk=1;
     rst=0;
     #(10) rst=1;
     #(30) rst=0;
   end
   
   always begin
    #(5) clk = ~clk;
    
   end //end always
   
   always begin
    
    #(50) ALUOp = ALUOp+1;
   end //end always
endmodule
