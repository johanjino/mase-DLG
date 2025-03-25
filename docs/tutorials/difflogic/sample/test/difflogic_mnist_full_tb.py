import os
import logging
from tqdm import tqdm
import torch
import numpy as np

import cocotb
import cocotb_test.simulator as simulator
from cocotb.clock import Clock
from cocotb.handle import HierarchyObject
from cocotb.triggers import RisingEdge, ClockCycles

async def init(dut: HierarchyObject) -> None:
    # Start clk
    await cocotb.start(Clock(dut.clk, 3.2, units = "ns").start())

    dut.rst.value = 1

    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 1)

    dut.rst.value = 0
    dut.data_out_0_ready.value = 1

import mnist_data
train_set = mnist_data.MNIST('./data-mnist', train=True, download=True, remove_border=True)
test_set = mnist_data.MNIST('./data-mnist', train=False, remove_border=True)
train_loader = torch.utils.data.DataLoader(train_set, batch_size=100, shuffle=True, pin_memory=True, drop_last=True, num_workers=4)
test_loader = torch.utils.data.DataLoader(test_set, batch_size=100, shuffle=False, pin_memory=True, drop_last=True)
dummy_in_loader = torch.utils.data.DataLoader(test_set, batch_size=1, shuffle=False, pin_memory=True, drop_last=True)


def sw2hw(img):
    out = []
    for row in img:
        num = ''
        for i in range(len(row)-1,-1,-1):
            num += str(row[i])
        num = int(num, 2)
        out.append(num)
    return out


INPUT_IMG = []
INPUT_LAB = []
for img, lab in dummy_in_loader:
    INPUT_IMG.append(img[0][0].round().int().tolist())
    INPUT_LAB.append(lab)


async def test_mnist_num_class(dut: HierarchyObject, num_img, expected_val: int) -> int:
    dut.data_in_0.value = sw2hw(num_img)
    await RisingEdge(dut.clk)
    await ClockCycles(dut.clk, 1)
    
    res = [int(str(_), 2) for _ in dut.data_out_0.value]
    res_max = max(res)
    res_ind = res.index(res_max)

    return (res_ind == expected_val)


@cocotb.test()
async def test_full_mnist(dut: HierarchyObject) -> None:
    await init(dut)
    
    count = 0
    
    for i in tqdm(range(len(INPUT_IMG))):
        count += await test_mnist_num_class(dut, INPUT_IMG[i], INPUT_LAB[i])
        
        await RisingEdge(dut.clk)
        await ClockCycles(dut.clk, 1)
        
    print(f"Total accuracy on MNIST: {count / len(INPUT_IMG)}")


def run_tests(log_level: int = logging.INFO, waves: bool = True):
    module = os.path.splitext(os.path.basename(__file__))[0]
    logging.getLogger('cocotb').setLevel(log_level)
    simulator.clean() 
    return simulator.run(toplevel="top_fake", module=module, waves=True)


if __name__ == "__main__":
    run_tests()
