-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-12-2021 a las 03:35:49
-- Versión del servidor: 10.4.22-MariaDB
-- Versión de PHP: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `robot`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `posicionmotores`
--

CREATE TABLE `posicionmotores` (
  `numero` int(11) NOT NULL,
  `motor_0` varchar(4) DEFAULT NULL,
  `motor_1` varchar(4) DEFAULT NULL,
  `motor_2` varchar(4) DEFAULT NULL,
  `motor_3` varchar(4) DEFAULT NULL,
  `motor_4` varchar(4) DEFAULT NULL,
  `motor_5` varchar(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `posicionmotores`
--

INSERT INTO `posicionmotores` (`numero`, `motor_0`, `motor_1`, `motor_2`, `motor_3`, `motor_4`, `motor_5`) VALUES
(3, '85', '133', '122', '0', '55', '150'),
(4, '85', '120', '115', '0', '55', '150'),
(5, '85', '133', '122', '0', '55', '90'),
(6, '85', '110', '122', '0', '55', '90'),
(7, '180', '120', '122', '0', '55', '90'),
(8, '180', '125', '122', '0', '55', '150'),
(10, '170', '120', '122', '0', '55', '90'),
(11, '170', '125', '122', '0', '55', '150'),
(12, '160', '120', '122', '0', '70', '90'),
(13, '160', '125', '122', '0', '70', '150'),
(14, '30', '110', '45', '0', '70', '45');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `posicionmotores`
--
ALTER TABLE `posicionmotores`
  ADD PRIMARY KEY (`numero`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `posicionmotores`
--
ALTER TABLE `posicionmotores`
  MODIFY `numero` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
