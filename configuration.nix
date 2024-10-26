{ ... }: {
  imports = [
    ./hardware-configuration.nix
    
    
  ];

  boot.tmp.cleanOnBoot = true;
  zramSwap.enable = true;
  networking.hostName = "eugenia";
  networking.domain = "";
  services.openssh.enable = true;
  users.users.root.openssh.authorizedKeys.keys = [''ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGqDnhdlknFB0KhLATaKouZW1jlqchpzuAcScrlOn4XG cdo@halley'' ];
  system.stateVersion = "23.11";
}
