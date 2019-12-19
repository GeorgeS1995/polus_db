-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Июл 07 2019 г., 12:33
-- Версия сервера: 5.5.60-MariaDB
-- Версия PHP: 7.3.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `polus_develop`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Assembly`
--

CREATE TABLE `Assembly` (
  `product_id` bigint(20) NOT NULL,
  `in_composition` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Characteristic_of_product`
--

CREATE TABLE `Characteristic_of_product` (
  `id` bigint(20) NOT NULL,
  `label` varchar(255) NOT NULL,
  `type_of_product_id` bigint(20) NOT NULL,
  `units` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Department`
--

CREATE TABLE `Department` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Employees`
--

CREATE TABLE `Employees` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `patronymic` varchar(255) NOT NULL,
  `rang_id` bigint(20) NOT NULL,
  `hash` varchar(128) NOT NULL,
  `salt` varchar(128) NOT NULL,
  `user_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Operation_history`
--

CREATE TABLE `Operation_history` (
  `id` bigint(20) NOT NULL,
  `start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `type_of_operation_id` bigint(20) NOT NULL,
  `type_of_defect_id` bigint(20) NOT NULL,
  `employess_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Product`
--

CREATE TABLE `Product` (
  `id` bigint(20) NOT NULL,
  `serial_number` varchar(255) NOT NULL,
  `type_of_product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Product_2_characteristic`
--

CREATE TABLE `Product_2_characteristic` (
  `product_id` bigint(20) NOT NULL,
  `characteristic_of_product_id` bigint(20) NOT NULL,
  `operation_history_id` bigint(20) NOT NULL,
  `value` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Rang`
--

CREATE TABLE `Rang` (
  `id` bigint(20) NOT NULL,
  `label` varchar(255) NOT NULL,
  `department_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Type_of_defect`
--

CREATE TABLE `Type_of_defect` (
  `id` bigint(20) NOT NULL,
  `label` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Type_of_operation`
--

CREATE TABLE `Type_of_operation` (
  `id` bigint(20) NOT NULL,
  `label` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Структура таблицы `Type_of_product`
--

CREATE TABLE `Type_of_product` (
  `id` bigint(20) NOT NULL,
  `model` varchar(255) NOT NULL,
  `department_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Assembly`
--
ALTER TABLE `Assembly`
  ADD KEY `fk_product_id` (`product_id`),
  ADD KEY `fk_product_in_composition` (`in_composition`);

--
-- Индексы таблицы `Characteristic_of_product`
--
ALTER TABLE `Characteristic_of_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_type_of_product_id` (`type_of_product_id`);

--
-- Индексы таблицы `Department`
--
ALTER TABLE `Department`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Employees`
--
ALTER TABLE `Employees`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_rang` (`rang_id`);

--
-- Индексы таблицы `Operation_history`
--
ALTER TABLE `Operation_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_employees_id` (`employess_id`),
  ADD KEY `fk_type_of_operation_id` (`type_of_operation_id`),
  ADD KEY `fk_type_of_defect_id` (`type_of_defect_id`);

--
-- Индексы таблицы `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_type_of_product_id_to_product` (`type_of_product_id`);

--
-- Индексы таблицы `Product_2_characteristic`
--
ALTER TABLE `Product_2_characteristic`
  ADD KEY `fk_characteristic_of_product_id` (`characteristic_of_product_id`),
  ADD KEY `fk_operation_history_id` (`operation_history_id`),
  ADD KEY `fk_product_id_to_p2c` (`product_id`);

--
-- Индексы таблицы `Rang`
--
ALTER TABLE `Rang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_department_id` (`department_id`);

--
-- Индексы таблицы `Type_of_defect`
--
ALTER TABLE `Type_of_defect`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Type_of_operation`
--
ALTER TABLE `Type_of_operation`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `Type_of_product`
--
ALTER TABLE `Type_of_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk` (`department_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Characteristic_of_product`
--
ALTER TABLE `Characteristic_of_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Department`
--
ALTER TABLE `Department`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Employees`
--
ALTER TABLE `Employees`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Operation_history`
--
ALTER TABLE `Operation_history`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Product`
--
ALTER TABLE `Product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Rang`
--
ALTER TABLE `Rang`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Type_of_defect`
--
ALTER TABLE `Type_of_defect`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Type_of_operation`
--
ALTER TABLE `Type_of_operation`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Type_of_product`
--
ALTER TABLE `Type_of_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Assembly`
--
ALTER TABLE `Assembly`
  ADD CONSTRAINT `fk_product_in_composition` FOREIGN KEY (`in_composition`) REFERENCES `Product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `Product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Characteristic_of_product`
--
ALTER TABLE `Characteristic_of_product`
  ADD CONSTRAINT `fk_type_of_product_id` FOREIGN KEY (`type_of_product_id`) REFERENCES `Type_of_product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Employees`
--
ALTER TABLE `Employees`
  ADD CONSTRAINT `fk_rang` FOREIGN KEY (`rang_id`) REFERENCES `Rang` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Operation_history`
--
ALTER TABLE `Operation_history`
  ADD CONSTRAINT `fk_type_of_defect_id` FOREIGN KEY (`type_of_defect_id`) REFERENCES `Type_of_defect` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_employees_id` FOREIGN KEY (`employess_id`) REFERENCES `Employees` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_type_of_operation_id` FOREIGN KEY (`type_of_operation_id`) REFERENCES `Type_of_operation` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Product`
--
ALTER TABLE `Product`
  ADD CONSTRAINT `fk_type_of_product_id_to_product` FOREIGN KEY (`type_of_product_id`) REFERENCES `Type_of_product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Product_2_characteristic`
--
ALTER TABLE `Product_2_characteristic`
  ADD CONSTRAINT `fk_product_id_to_p2c` FOREIGN KEY (`product_id`) REFERENCES `Product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_characteristic_of_product_id` FOREIGN KEY (`characteristic_of_product_id`) REFERENCES `Characteristic_of_product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_operation_history_id` FOREIGN KEY (`operation_history_id`) REFERENCES `Operation_history` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Rang`
--
ALTER TABLE `Rang`
  ADD CONSTRAINT `fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `Department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `Type_of_product`
--
ALTER TABLE `Type_of_product`
  ADD CONSTRAINT `fk` FOREIGN KEY (`department_id`) REFERENCES `Department` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
