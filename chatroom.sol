// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.4.16 < 0.9.0;

struct Message {
    address addr;
    string nickname;
    string contents;
}

contract Chatroom {

    Message[] public messages;

    event NewMessage(Message);

    function sendMessage(string memory nickname, string memory contents) public {
        messages.push(Message(msg.sender, nickname, contents));
        emit NewMessage(messages[messages.length - 1]);
    }

    function getMessageCount() public view returns (uint) {
        return messages.length;
    }
}
