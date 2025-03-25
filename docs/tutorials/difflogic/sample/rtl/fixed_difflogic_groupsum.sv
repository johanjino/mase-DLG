module fixed_difflogic_groupsum #(
    parameter DATA_IN_0_TENSOR_SIZE_DIM_0 = 4,
    parameter DATA_OUT_0_TENSOR_SIZE_DIM_0 = 2
) (
    input  logic                 clk,
    input  logic                 rst,

    input  logic [DATA_IN_0_TENSOR_SIZE_DIM_0-1:0]  data_in_0,
    input  logic data_in_0_valid,
    output logic data_in_0_ready,

    output logic [$clog2((DATA_IN_0_TENSOR_SIZE_DIM_0 / DATA_OUT_0_TENSOR_SIZE_DIM_0)):0] data_out_0 [0:DATA_OUT_0_TENSOR_SIZE_DIM_0-1],
    output logic data_out_0_valid,
    input  logic data_out_0_ready
);

    localparam GROUP_SIZE = DATA_IN_0_TENSOR_SIZE_DIM_0 / DATA_OUT_0_TENSOR_SIZE_DIM_0;

    genvar i;
    generate
        for (i = 0; i < DATA_OUT_0_TENSOR_SIZE_DIM_0; i = i + 1) begin : GROUP_SUM
            logic [GROUP_SIZE-1:0] group_data;
            logic [$clog2(GROUP_SIZE):0] sum;

            assign group_data = data_in_0[((i * GROUP_SIZE) + (GROUP_SIZE-1)): (i * GROUP_SIZE)];
            
            always_comb begin
                data_out_0[i] = $countones(group_data);
            end
        end
    endgenerate

    assign data_out_0_valid= data_in_0_valid;
    assign data_in_0_ready = data_out_0_ready;

endmodule
