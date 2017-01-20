-- phpMyAdmin SQL Dump
-- version phpStudy 2014
-- http://www.phpmyadmin.net
--
-- 主机: 127.0.0.1
-- 生成日期: 2017-01-20 18:28:33
-- 服务器版本: 5.5.36-log
-- PHP 版本: 5.5.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `kakamaifang`
--

-- --------------------------------------------------------

--
-- 表的结构 `kk_house`
--

CREATE TABLE IF NOT EXISTS `kk_house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(30) NOT NULL COMMENT '名称',
  `url` varchar(255) NOT NULL COMMENT '链接',
  `sourceId` varchar(255) NOT NULL COMMENT '房产id',
  `houseInfo` varchar(50) NOT NULL COMMENT '房产信息',
  `dealDate` varchar(15) NOT NULL COMMENT '成交日期',
  `totalPrice` varchar(5) NOT NULL COMMENT '成交价格',
  `totalPriceUnit` varchar(5) NOT NULL COMMENT '成交价格单位',
  `positionInfo` varchar(50) NOT NULL COMMENT '楼层信息',
  `source` varchar(20) NOT NULL COMMENT '链家成交',
  `unitPrice` varchar(11) NOT NULL COMMENT '单价',
  `unitPriceUnit` varchar(10) DEFAULT NULL COMMENT '单价单位',
  `dealHouseTxt` varchar(255) DEFAULT NULL COMMENT '地铁信息',
  `compound` varchar(50) DEFAULT NULL COMMENT '小区名称',
  `layout` varchar(10) DEFAULT NULL COMMENT '户型',
  `space` varchar(10) DEFAULT NULL COMMENT '面积',
  `rowards` varchar(10) DEFAULT NULL COMMENT '朝向',
  `renovation` varchar(10) DEFAULT NULL COMMENT '装修',
  `elevator` varchar(10) DEFAULT NULL COMMENT '电梯',
  `number` varchar(10) DEFAULT NULL COMMENT '楼层',
  `age` varchar(10) DEFAULT NULL COMMENT '年代',
  `buildings` varchar(10) DEFAULT NULL COMMENT '建筑形状',
  `area` varchar(5) DEFAULT NULL COMMENT '行政区',
  `trade` varchar(20) DEFAULT NULL COMMENT '商圈',
  `ditie` varchar(10) DEFAULT NULL COMMENT '几号线地铁',
  `ditiezhan` varchar(20) DEFAULT NULL COMMENT '地铁站',
  `ditiejianju` varchar(20) DEFAULT NULL COMMENT '地铁间距',
  `zhengce` varchar(10) DEFAULT NULL COMMENT '政策',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8493 ;
