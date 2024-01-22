
  module RF(   input         clk, 
               input         rst,
               input         RFWr, 
               input  [4:0]  A1, A2, A3, 
               input  [31:0] WD, 
               input  DM_SH,
               input  DM_SB,
               output [31:0] RD1, RD2,
               input  [4:0]  reg_sel,
               output [31:0] reg_data,
               output [31:0]temp,
               input RF_U
               
);

  reg [31:0] rf[31:0];

  integer i;
  assign temp=rf[A3];

  always @(posedge clk, posedge rst)
    if (rst) begin    //  reset
      for (i=1; i<32; i=i+1)
        rf[i] <= 0; //  i;
               end
      
    else 
        begin
             if (RFWr&~RF_U) 
                 begin
                  rf[A3] <= {32{~DM_SH&~DM_SB}}& WD   |
                                  {32{DM_SH}} & { temp[31:16] , WD[15:0]    } |
                                  {32{DM_SB}} &{temp[31:8], WD[7:0]} ;
                  $display("r[%2d] = 0x%8X,", A3, WD);
                 end
             if (RFWr&RF_U) 
               begin
                  rf[A3] <= {32{~DM_SH&~DM_SB}}& WD   |
                                  {32{DM_SH}} & { {16{0}} , WD[15:0]    } |
                                  {32{DM_SB}} &{{24{0}}, WD[7:0]} ;
                  $display("r[%2d] = 0x%8X,", A3, WD);
               end
       end

  assign RD1 = (A1 != 0) ? rf[A1] : 0;
  assign RD2 = (A2 != 0) ? rf[A2] : 0;
  assign reg_data = (reg_sel != 0) ? rf[reg_sel] : 0; 

endmodule 
