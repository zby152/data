`timescale 1ns / 1ps

module alu_tb();

reg signed [31:0]A,B;
reg [3:0]ALUOp;
wire [31:0]C;
wire Zero;

alu U_ALL(.A(A), .B(B), .ALUOp(ALUOp), .Zero(Zero), .C(C));

initial 
begin
A=32'd2;
B=32'd1;
ALUOp=4'b1000;
end

always #50 A=A+1;

endmodule

