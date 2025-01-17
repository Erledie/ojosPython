-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 17-01-2025 a las 18:13:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `registro_ingresos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresos`
--

CREATE TABLE `ingresos` (
  `id_ingreso` int(11) NOT NULL,
  `llave_ingreso` int(11) NOT NULL,
  `fecha_ingreso` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ingresos`
--

INSERT INTO `ingresos` (`id_ingreso`, `llave_ingreso`, `fecha_ingreso`) VALUES
(3, 39, '2025-01-17 16:01:50'),
(4, 40, '2025-01-17 16:02:11'),
(5, 41, '2025-01-17 16:02:56'),
(6, 42, '2025-01-17 16:03:25'),
(7, 42, '2025-01-17 16:03:45'),
(8, 43, '2025-01-17 16:04:42'),
(9, 43, '2025-01-17 16:05:22'),
(10, 43, '2025-01-17 16:06:34'),
(11, 43, '2025-01-17 16:06:38'),
(12, 43, '2025-01-17 16:06:42'),
(13, 43, '2025-01-17 16:06:46'),
(14, 43, '2025-01-17 16:06:50'),
(15, 43, '2025-01-17 16:06:54'),
(16, 43, '2025-01-17 16:06:58'),
(17, 43, '2025-01-17 16:07:02'),
(18, 43, '2025-01-17 16:07:06'),
(19, 43, '2025-01-17 16:07:10'),
(20, 43, '2025-01-17 16:07:14'),
(21, 43, '2025-01-17 16:07:18');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `llaves`
--

CREATE TABLE `llaves` (
  `id_llave` int(11) NOT NULL,
  `llave_tipo` varchar(20) NOT NULL,
  `dato_llave` varchar(20) DEFAULT NULL,
  `fecha_creacion` timestamp NOT NULL DEFAULT current_timestamp(),
  `ruta_llave` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `llaves`
--

INSERT INTO `llaves` (`id_llave`, `llave_tipo`, `dato_llave`, `fecha_creacion`, `ruta_llave`) VALUES
(39, 'Documento', '1003912743', '2025-01-17 16:01:50', 'D:/Ideas-tico/tarea-1/cedulas\\doc_imgp_20250117_110149.jpg'),
(40, 'Documento', '1003912749', '2025-01-17 16:02:11', 'D:/Ideas-tico/tarea-1/cedulas\\doc_imgp_20250117_110211.jpg'),
(41, 'Documento', '1234567869', '2025-01-17 16:02:56', 'D:/Ideas-tico/tarea-1/cedulas\\doc_imgp_20250117_110256.jpg'),
(42, 'Documento', '1234567890', '2025-01-17 16:03:25', 'D:/Ideas-tico/tarea-1/cedulas\\doc_imgp_20250117_110325.jpg'),
(43, 'Qr', '100010001001', '2025-01-17 16:04:42', 'Pendiente');

--
-- Disparadores `llaves`
--
DELIMITER $$
CREATE TRIGGER `registro_ingreso` AFTER INSERT ON `llaves` FOR EACH ROW BEGIN
    INSERT INTO ingresos (llave_ingreso, fecha_ingreso)
    VALUES (NEW.id_llave, NOW());
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `llaves_no_registradas`
--

CREATE TABLE `llaves_no_registradas` (
  `id_llave_nr` int(11) NOT NULL,
  `llave_tipo_nr` varchar(20) DEFAULT NULL,
  `dato_llave_nr` varchar(20) DEFAULT NULL,
  `fecha_registro_nr` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `llaves_no_registradas`
--

INSERT INTO `llaves_no_registradas` (`id_llave_nr`, `llave_tipo_nr`, `dato_llave_nr`, `fecha_registro_nr`) VALUES
(10, 'Documento', '1234567689', '2025-01-17 16:08:07'),
(11, 'Documento', '1090908900', '2025-01-17 16:09:01');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ingresos`
--
ALTER TABLE `ingresos`
  ADD PRIMARY KEY (`id_ingreso`),
  ADD KEY `llave_ingreso` (`llave_ingreso`);

--
-- Indices de la tabla `llaves`
--
ALTER TABLE `llaves`
  ADD PRIMARY KEY (`id_llave`);

--
-- Indices de la tabla `llaves_no_registradas`
--
ALTER TABLE `llaves_no_registradas`
  ADD PRIMARY KEY (`id_llave_nr`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ingresos`
--
ALTER TABLE `ingresos`
  MODIFY `id_ingreso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `llaves`
--
ALTER TABLE `llaves`
  MODIFY `id_llave` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT de la tabla `llaves_no_registradas`
--
ALTER TABLE `llaves_no_registradas`
  MODIFY `id_llave_nr` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ingresos`
--
ALTER TABLE `ingresos`
  ADD CONSTRAINT `ingresos_ibfk_1` FOREIGN KEY (`llave_ingreso`) REFERENCES `llaves` (`id_llave`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
