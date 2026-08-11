// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

#include "quiche/quic/core/congestion_control/send_algorithm_interface.h"

#include "absl/base/attributes.h"
#include "quiche/quic/core/congestion_control/bbr2_sender.h"
#include "quiche/quic/core/congestion_control/bbr_sender.h"
#include "quiche/quic/core/congestion_control/tcp_cubic_sender_bytes.h"
#include "quiche/quic/core/quic_packets.h"
#include "quiche/quic/platform/api/quic_bug_tracker.h"
#include "quiche/quic/platform/api/quic_flag_utils.h"
#include "quiche/quic/platform/api/quic_flags.h"

namespace quic {

class RttStats;

// Factory for send side congestion control algorithm.
SendAlgorithmInterface* SendAlgorithmInterface::Create(
    const QuicClock* clock, const RttStats* rtt_stats,
    const QuicUnackedPacketMap* unacked_packets,
    CongestionControlType congestion_control_type, QuicRandom* random,
    QuicConnectionStats* stats, QuicPacketCount initial_congestion_window,
    SendAlgorithmInterface* old_send_algorithm) {
  QuicPacketCount max_congestion_window =
      GetQuicFlag(quic_max_congestion_window);
      
     if((congestion_control_type == kGoogCC)|| (congestion_control_type == kBBR)||(congestion_control_type == kBBRv2)||(congestion_control_type == kPCC)||(congestion_control_type == kCubicBytes)||(congestion_control_type == kRenoBytes)){
      //std::cout<<"Cubic";
      return new TcpCubicSenderBytes(clock, rtt_stats, true /* use Reno */,
                                     initial_congestion_window,
                                     max_congestion_window, stats);}
       else{
       std::cout<<"CFAILED";
       return nullptr;}
       
}

}  // namespace quic
