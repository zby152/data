
// data memory
module dm(clk, DMWr, addr, din, dout,DM_SH,DM_SB);
   input          clk;
   input          DMWr;
   input  [8:2]   addr;
   input  [31:0]  din;
   input DM_SH;
   input DM_SB;
   output [31:0]  dout;
     
   reg [31:0] dmem[127:0];
   wire [31:0] addrByte;

   assign addrByte = addr<<2;
      
   assign dout = dmem[addrByte[8:2]];
   
   always @(posedge clk)
      if (DMWr) begin
        dmem[addrByte[8:2]] <={32{~DM_SH&~DM_SB}}&din   |
                                                {32{DM_SH}} & { dout[31:16] , din[15:0]    } |
                                                {32{DM_SB}} &{dout[31:8], din[7:0]} ;
        $display("dmem[0x%8X] = 0x%8X,", addrByte, din); 
      end
   
endmodule    
