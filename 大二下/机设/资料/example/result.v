module result( clk, rst, aluoutC, Result );

  input              clk;
  input              rst;
  input       [31:0] aluoutC;
  output reg  [31:0] Result;

  always @(posedge clk, posedge rst)
    if (rst) 
      Result <= 32'h0000_0000;
    else
      Result <= aluoutC;
      
endmodule

